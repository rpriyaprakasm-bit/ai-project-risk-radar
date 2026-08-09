"""
Loop layer: evidence-based verification before publish/commit.
Fails the job only on hard schema breaks; soft issues are warnings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_TOP = ["date", "overall_risk_level", "summary", "risks"]
ALLOWED_SEVERITY = {"Critical", "High", "Medium", "Low"}
ALLOWED_CATEGORY = {
    "Schedule",
    "Blocker",
    "Scope",
    "People",
    "Quality",
    "Communication",
}


def verify(path: Path = Path("data/risk_report.json")) -> int:
    errors: List[str] = []
    warnings: List[str] = []

    if not path.exists():
        print(f"ERROR: missing {path}", file=sys.stderr)
        return 1

    try:
        data: Dict[str, Any] = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        return 1

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    level = data.get("overall_risk_level")
    if level and level not in ALLOWED_SEVERITY:
        errors.append(f"invalid overall_risk_level: {level}")

    risks = data.get("risks")
    if not isinstance(risks, list):
        errors.append("risks must be a list")
        risks = []
    elif len(risks) == 0:
        warnings.append("risks list is empty")

    for i, r in enumerate(risks):
        if not isinstance(r, dict):
            errors.append(f"risks[{i}] is not an object")
            continue
        if not r.get("title"):
            errors.append(f"risks[{i}] missing title")
        sev = r.get("severity")
        if sev and sev not in ALLOWED_SEVERITY:
            errors.append(f"risks[{i}] invalid severity: {sev}")
        cat = r.get("category")
        if cat and cat not in ALLOWED_CATEGORY:
            warnings.append(f"risks[{i}] unusual category: {cat}")

    source = data.get("source", "unknown")
    md = Path("data/risk_report.md")
    if not md.exists() or md.stat().st_size < 20:
        errors.append("risk_report.md missing or too short")

    print("=== Risk report verification ===")
    print(f"source={source} overall={data.get('overall_risk_level')} risks={len(risks)}")
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print("Verification FAILED — fix report before publish.")
        return 1

    print("Verification PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
