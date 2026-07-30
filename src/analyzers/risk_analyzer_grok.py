"""
Grok-powered Risk Analyzer (xAI).
Reads project data and produces a structured Risk Report + JSON for the dashboard.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI


def analyze():
    data_path = Path("data/project_data.json")
    if not data_path.exists():
        raise FileNotFoundError("No project data found. Run the collector first.")

    project_data = json.loads(data_path.read_text())

    prompt_path = Path("prompts/risk_analysis.md")
    system_prompt = prompt_path.read_text() if prompt_path.exists() else (
        "You are an expert project risk analyst. Produce a clear Markdown risk report."
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

    client = OpenAI(
        api_key=os.environ.get("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )

    print("Sending data to Grok for risk analysis...")
    response = client.chat.completions.create(
        model="grok-4.5",
        max_tokens=3000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    full_text = response.choices[0].message.content or ""

    # Save full Markdown report (strip the JSON block for clean MD if present)
    md_report = full_text
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", full_text, re.DOTALL)
    if json_match:
        md_report = full_text[: json_match.start()].strip()

    out_md = Path("data/risk_report.md")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md_report)
    print(f"Risk report written → {out_md}")

    # Extract / save structured JSON for the dashboard
    risk_json = None
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
            "raw_markdown": md_report,
        }

    out_json = Path("data/risk_report.json")
    out_json.write_text(json.dumps(risk_json, indent=2))
    print(f"Structured risk data written → {out_json}")

    return md_report, risk_json


if __name__ == "__main__":
    analyze()
