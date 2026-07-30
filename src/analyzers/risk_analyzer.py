"""
Claude-powered Risk Analyzer.
Reads project data and produces a structured Risk Report.
"""

import json
import os
from pathlib import Path

from anthropic import Anthropic


def analyze():
    data_path = Path("data/project_data.json")
    if not data_path.exists():
        raise FileNotFoundError("No project data found. Run the collector first.")

    project_data = json.loads(data_path.read_text())

    prompt_path = Path("prompts/risk_analysis.md")
    system_prompt = prompt_path.read_text() if prompt_path.exists() else "You are an expert project risk analyst."

    user_content = f"""Analyze the following project data and produce a Risk Report following the required format.

PROJECT DATA:
{json.dumps(project_data, indent=2)}
"""

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print("Sending data to Claude for risk analysis...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )

    report = message.content[0].text

    out_path = Path("data/risk_report.md")
    out_path.write_text(report)
    print(f"Risk report written → {out_path}")
    return report


if __name__ == "__main__":
    analyze()
