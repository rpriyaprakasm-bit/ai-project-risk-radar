"""
Grok-powered Risk Analyzer (xAI).
Reads project data and produces a structured Risk Report + JSON for the dashboard.

If XAI_API_KEY is missing or the xAI API fails (e.g. no credits / 403),
falls back to a local heuristic report so the workflow still completes.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI


def analyze() -> Tuple[str, Dict[str, Any]]:
    data_path = Path("data/project_data.json")
    if not data_path.exists():
        raise FileNotFoundError("No project data found. Run the collector first.")

    project_data = json.loads(data_path.read_text())

    api_key = (os.environ.get("XAI_API_KEY") or "").strip()
    if not api_key:
        print(
            "WARNING: XAI_API_KEY is not set. Using local heuristic fallback.",
            file=sys.stderr,
        )
        return _write_outputs(*_heuristic_report(project_data, reason="XAI_API_KEY not set"))

    prompt_path = Path("prompts/risk_analysis.md")
    system_prompt = (
        prompt_path.read_text()
        if prompt_path.exists()
        else "You are an expert project risk analyst. Produce a clear Markdown risk report."
    )

    user_content = f"""Analyze the following project data and produce a Risk Report following the required format.

PROJECT DATA:
{json.dumps(project_data, indent=2)}

IMPORTANT: After the Markdown report, also output a machine-readable JSON block
exactly like this (no extra text around it):

```json
{{
  "date": "YYYY-MM-DD",
  "overall_risk_level": "Critical|High|Medium|Low",
  "summary": "...",
  "risks": [
    {{
      "title": "...",
      "category": "Schedule|Blocker|Scope|People|Quality|Communication",
      "severity": "Critical|High|Medium|Low",
      "confidence": "High|Medium|Low",
      "evidence": "...",
      "recommended_action": "..."
    }}
  ],
  "positive_signals": ["..."],
  "trend": "increasing|stable|decreasing",
  "trend_explanation": "...",
  "next_steps": ["...", "..."]
}}
```
"""

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    model = os.environ.get("XAI_MODEL", "grok-3")

    print(f"Sending data to Grok ({model}) for risk analysis...")
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=3000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
    except Exception as e:
        err = str(e)
        print(f"WARNING: xAI API call failed: {err}", file=sys.stderr)
        print("Falling back to local heuristic risk report so the pipeline can continue.")
        reason = "xAI API error"
        if "403" in err or "permission-denied" in err.lower() or "credits" in err.lower():
            reason = "xAI team has no credits/licenses (403)"
        return _write_outputs(*_heuristic_report(project_data, reason=reason))

    full_text = response.choices[0].message.content or ""

    md_report = full_text
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", full_text, re.DOTALL)
    if json_match:
        md_report = full_text[: json_match.start()].strip()

    risk_json: Optional[Dict[str, Any]] = None
    if json_match:
        try:
            risk_json = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            print("Warning: could not parse JSON block from Grok response")

    if not risk_json:
        risk_json = {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "overall_risk_level": "Medium",
            "summary": "Structured JSON was not returned; see the Markdown report.",
            "risks": [],
            "positive_signals": [],
            "trend": "stable",
            "trend_explanation": "",
            "next_steps": [],
            "source": "grok",
            "raw_markdown": md_report,
        }
    else:
        risk_json.setdefault("source", "grok")

    return _write_outputs(md_report, risk_json)


def _heuristic_report(project_data: Dict[str, Any], reason: str) -> Tuple[str, Dict[str, Any]]:
    """Rule-based report from issues/PRs when Grok is unavailable."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    issues = project_data.get("issues") or []
    prs = project_data.get("pull_requests") or []
    meta = project_data.get("metadata") or {}
    source = project_data.get("source") or "unknown"

    risks: List[Dict[str, Any]] = []

    for issue in issues:
        labels = [str(l).lower() for l in (issue.get("labels") or [])]
        title = issue.get("title") or f"Issue #{issue.get('id')}"
        body = (issue.get("body") or "")[:300]
        assignees = issue.get("assignees") or []
        due = issue.get("due_date")
        comments = issue.get("comments_count") or 0

        severity = "Medium"
        category = "Scope"
        if any(x in labels for x in ("blocker", "blocked", "critical")):
            severity = "Critical"
            category = "Blocker"
        elif any(x in labels for x in ("high-priority", "high", "urgent")):
            severity = "High"
        elif any(x in labels for x in ("bug", "quality", "flaky")):
            category = "Quality"
            severity = "High" if comments >= 8 else "Medium"
        elif any(x in labels for x in ("feature", "unestimated")):
            category = "Scope"
        elif "database" in labels or "migration" in title.lower():
            category = "Schedule"
            severity = "High"

        if due and due < today and (issue.get("state") or "").lower() == "open":
            severity = "Critical" if severity != "Critical" else severity
            category = "Schedule"

        if not assignees and severity in ("Critical", "High"):
            people_note = " No assignee."
        else:
            people_note = ""

        risks.append(
            {
                "title": title,
                "category": category,
                "severity": severity,
                "confidence": "Medium",
                "evidence": (
                    f"Labels: {', '.join(labels) or 'none'}. "
                    f"Comments: {comments}. Due: {due or 'n/a'}."
                    f"{people_note} {body}"
                ).strip(),
                "recommended_action": _suggest_action(severity, category, assignees, due),
            }
        )

    for pr in prs:
        labels = [str(l).lower() for l in (pr.get("labels") or [])]
        title = pr.get("title") or f"PR #{pr.get('id')}"
        if "wip" in labels or title.lower().startswith("wip"):
            risks.append(
                {
                    "title": f"Long-running WIP PR: {title}",
                    "category": "Schedule",
                    "severity": "Medium",
                    "confidence": "Medium",
                    "evidence": f"Open PR by {pr.get('user') or 'unknown'}; labels: {', '.join(labels) or 'none'}.",
                    "recommended_action": "Time-box remaining work or split into reviewable PRs.",
                }
            )

    # Key-person concentration
    assignee_counts: Dict[str, int] = {}
    for issue in issues:
        for a in issue.get("assignees") or []:
            assignee_counts[a] = assignee_counts.get(a, 0) + 1
    for person, count in assignee_counts.items():
        if count >= 3:
            risks.append(
                {
                    "title": f"Key-person load on {person}",
                    "category": "People",
                    "severity": "High",
                    "confidence": "High",
                    "evidence": f"{person} is assigned to {count} open items.",
                    "recommended_action": f"Rebalance work away from {person} or add backup owners.",
                }
            )

    if not risks:
        risks.append(
            {
                "title": "Limited signal in collected data",
                "category": "Communication",
                "severity": "Low",
                "confidence": "Low",
                "evidence": f"Source={source}; open issues={meta.get('open_issues_count', len(issues))}.",
                "recommended_action": "Confirm trackers are up to date; re-run after new issues land.",
            }
        )

    rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    risks.sort(key=lambda r: rank.get(r.get("severity") or "Low", 9))

    severities = [r["severity"] for r in risks]
    if "Critical" in severities:
        overall = "Critical"
    elif severities.count("High") >= 2 or "High" in severities:
        overall = "High"
    elif "Medium" in severities:
        overall = "Medium"
    else:
        overall = "Low"

    summary = (
        f"Local heuristic analysis ({reason}). "
        f"Overall risk {overall} from {len(issues)} issues and {len(prs)} PRs. "
        f"Top themes: {', '.join(sorted({r['category'] for r in risks[:5]}))}."
    )

    positive = []
    if any("frontend" in [str(l).lower() for l in (i.get("labels") or [])] for i in issues):
        positive.append("Some work items are labeled and trackable.")
    if meta.get("open_prs_count") or prs:
        positive.append("Delivery activity visible via open pull requests.")
    if not positive:
        positive.append("Structured issue data was available for rule-based scoring.")

    next_steps = [
        "Address Critical/High items first (blockers and overdue dates).",
        "Assign owners where missing on high-severity issues.",
        "Add xAI credits at console.x.ai to enable full Grok analysis on the next run.",
    ]

    risk_json: Dict[str, Any] = {
        "date": today,
        "overall_risk_level": overall,
        "summary": summary,
        "risks": risks[:12],
        "positive_signals": positive,
        "trend": "stable",
        "trend_explanation": "Heuristic single-snapshot analysis; no multi-week history.",
        "next_steps": next_steps,
        "source": "heuristic-fallback",
        "fallback_reason": reason,
    }

    md_lines = [
        f"# Project Risk Report — {today}",
        "",
        f"> **Mode:** Local heuristic fallback ({reason}).  ",
        "> Grok analysis was skipped or unavailable. Add xAI credits to enable AI narrative.",
        "",
        f"## Overall risk: **{overall}**",
        "",
        summary,
        "",
        "## Risks",
        "",
    ]
    for i, r in enumerate(risks[:12], 1):
        md_lines.append(
            f"### {i}. [{r['severity']}] {r['title']}\n"
            f"- **Category:** {r['category']}  \n"
            f"- **Evidence:** {r['evidence']}  \n"
            f"- **Action:** {r['recommended_action']}\n"
        )

    md_lines.extend(
        [
            "## Positive signals",
            "",
            *[f"- {p}" for p in positive],
            "",
            "## Next steps",
            "",
            *[f"{i}. {s}" for i, s in enumerate(next_steps, 1)],
            "",
        ]
    )

    return "\n".join(md_lines), risk_json


def _suggest_action(
    severity: str, category: str, assignees: List[str], due: Optional[str]
) -> str:
    if category == "Blocker":
        return "Escalate blocker owner and set a dated resolution plan within 48 hours."
    if category == "Schedule" and due:
        return f"Re-baseline the date past {due} or cut scope; name a single accountable owner."
    if category == "People" or not assignees:
        return "Assign a primary owner and a backup; protect capacity for critical path."
    if category == "Quality":
        return "Quarantine flaky tests or fix within one sprint; stop silent CI noise."
    if severity in ("Critical", "High"):
        return "Bring to weekly risk review with a clear ask and owner."
    return "Track in backlog with next review date."


def _write_outputs(md_report: str, risk_json: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    out_md = Path("data/risk_report.md")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md_report)
    print(f"Risk report written → {out_md}")

    out_json = Path("data/risk_report.json")
    out_json.write_text(json.dumps(risk_json, indent=2))
    print(f"Structured risk data written → {out_json} (source={risk_json.get('source')})")
    return md_report, risk_json


if __name__ == "__main__":
    analyze()
