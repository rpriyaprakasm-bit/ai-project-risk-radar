# AI Project Risk Radar

> An intelligent early-warning system that automatically detects project risks before they become expensive problems.

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Claude](https://img.shields.io/badge/Powered%20by-Claude-D97757?logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![Extensible](https://img.shields.io/badge/Supports-GitHub%20%7C%20Jira%20%7C%20Linear%20%7C%20Notion-blue)](#extending-to-other-tools)

---

## The Real Problem

Most projects don’t fail because of one big disaster.  
They fail because small risks slowly accumulate and nobody notices early enough.

Project managers spend hours every week manually scanning tickets, comments, and schedules looking for trouble. By the time a risk becomes obvious, it is usually already costly.

**This tool solves that.**

---

## What It Does

The **AI Project Risk Radar** automatically analyzes your project data and produces a clear, prioritized Risk Report that includes:

- Overall Risk Level (Low / Medium / High / Critical)
- Prioritized list of detected risks
- Evidence for each risk
- Recommended actions
- Trend indicators

### Risk Categories Detected

| Category | What it looks for |
|----------|-------------------|
| **Schedule Risk** | Overdue tasks, slipping deadlines |
| **Blocker Risk** | Growing number of blocked items |
| **Scope Risk** | Sudden increase in unestimated work |
| **People Risk** | Critical work concentrated on too few people |
| **Quality Risk** | Rising bugs or failing checks |
| **Communication Risk** | Important tickets going silent |

---

## Architecture (Designed for Extensibility)

```
┌─────────────────────┐
│  Data Collectors    │  ← GitHub (ready) | Jira / Linear / Notion (easy to add)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Risk Analyzer      │  ← Claude (structured risk analysis)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Report Generator   │  ← Markdown + GitHub Issue
└─────────────────────┘
```

The collector layer is modular. You can add new tools without rewriting the core logic.

---

## Quick Start

1. **Fork or clone** this repository
2. Add your `ANTHROPIC_API_KEY` as a GitHub Actions secret
3. (Optional) Adjust the schedule in `.github/workflows/risk-radar.yml`
4. The workflow will run automatically and post a Risk Report as a GitHub Issue

> You can also trigger it manually from the Actions tab.

---

## Example Output

See [`examples/sample-risk-report.md`](examples/sample-risk-report.md) for a realistic example of what the radar produces.

---

## Project Structure

```text
ai-project-risk-radar/
├── .github/workflows/
│   └── risk-radar.yml          # Scheduled + manual trigger
├── src/
│   ├── collectors/             # Data sources (modular)
│   │   ├── github_collector.py
│   │   ├── base.py
│   │   └── stubs/              # Ready for Jira, Linear, Notion
│   ├── analyzers/
│   │   └── risk_analyzer.py    # Claude-powered analysis
│   └── reporters/
│       └── report_generator.py
├── prompts/
│   └── risk_analysis.md        # High-quality system prompt
├── examples/
│   └── sample-risk-report.md
├── docs/
│   ├── architecture.md
│   └── extending.md            # How to add Jira / Linear / Notion
└── README.md
```

---

## Extending to Other Tools

The system is deliberately modular.

To add **Jira**, **Linear**, or **Notion**:

1. Create a new collector in `src/collectors/` that implements the same interface
2. Return data in the standard format (see `docs/extending.md`)
3. Register it in the workflow

No changes needed to the Risk Analyzer or Report Generator.

---

## Skills Demonstrated

- Agentic AI system design
- Structured output & prompt engineering
- Modular software architecture
- GitHub Actions automation
- Real-world problem solving in Project Management
- Extensibility and clean interfaces

---

## License

MIT

---

**Built to show that AI can do more than generate text — it can actively protect projects.**
