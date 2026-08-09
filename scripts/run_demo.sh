#!/usr/bin/env bash
# HARNESS: local one-command demo for AI Project Risk Radar
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== AI Project Risk Radar — local demo harness ==="
python3 -m src.collectors.github_collector
python3 -m src.analyzers.risk_analyzer_grok
python3 -m src.validators.verify_risk_report
echo ""
echo "Report: data/risk_report.md"
echo "JSON:   data/risk_report.json"
if [ -f dashboard/index.html ]; then
  echo "Dashboard: open dashboard/index.html in a browser"
fi
echo "Done."
