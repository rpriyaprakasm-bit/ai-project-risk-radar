# Agent layers — AI Project Risk Radar

Mapped to harness / loop / graph engineering.

## Harness (environment)

| Capability | Where |
|------------|--------|
| Tools | GitHub API collector, xAI chat API, issue publisher |
| State | `data/project_data.json`, `data/risk_report.*`, `dashboard/` |
| Secrets | `XAI_API_KEY`, `GITHUB_TOKEN` |
| Fallback | Demo issues when repo empty; heuristic report when xAI has no credits |
| Local entry | `scripts/run_demo.sh` |

## Loop (feedback)

| Step | Evidence |
|------|----------|
| Collect | `project_data.json` exists |
| Analyze | `risk_report.json` + `.md` written |
| **Verify** | `src/validators/verify_risk_report.py` — schema, severities, non-empty risks |
| Publish | Issue created (non-blocking if API fails) |
| Stop | Max one analysis pass per run; no unbounded retries |

## Graph (control flow)

```text
Checkout → Python → Collect
                ↓
         Analyze (Grok)
           ↙        ↘
      success     API fail
           ↘        ↙
         Heuristic fallback
                ↓
            Verify ──fail──→ job fails (no bad publish)
                ↓ pass
         Publish Issue (continue-on-error)
                ↓
         Dashboard + Commit
                ↓
            Summary (always)
```

## Diagnose failures

| Symptom | Layer to fix |
|---------|----------------|
| Missing files / permissions | Harness |
| Empty or invalid report | Loop (verify) |
| Wrong step order / skipped publish | Graph |
| Weak narrative only | Model / prompt (after harness+loop OK) |
