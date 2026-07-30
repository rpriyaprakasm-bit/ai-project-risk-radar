# AI Project Risk Radar

> An intelligent early-warning system that automatically detects project risks before they become expensive problems.

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)
[![Claude](https://img.shields.io/badge/Also%20supports-Claude-D97757?logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![Dashboard](https://img.shields.io/badge/Interactive-Dashboard-38bdf8)](https://htmlpreview.github.io/?https://github.com/rpriyaprakasm-bit/ai-project-risk-radar/blob/main/dashboard/index.html)
[![Extensible](https://img.shields.io/badge/Supports-GitHub%20%7C%20Jira%20%7C%20Linear%20%7C%20Notion-blue)](#extending-to-other-tools)

---

## The Real Problem

Most projects don’t fail because of one big disaster.  
They fail because small risks slowly accumulate and nobody notices early enough.

Project managers spend hours every week manually scanning tickets, comments, and schedules looking for trouble. By the time a risk becomes obvious, it is usually already costly.

**This tool solves that.**

---

## What It Does

The **AI Project Risk Radar** automatically analyzes your project data and produces:

1. A clear **Risk Report** (Markdown + GitHub Issue)
2. Structured **JSON** for automation
3. An interactive **Risk Dashboard**

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

## Live Dashboard

**GitHub does not run HTML files when you click them in the repo** — it only shows the source code.

### View the dashboard right now (click this):

**→ [Open Interactive Risk Dashboard](https://htmlpreview.github.io/?https://github.com/rpriyaprakasm-bit/ai-project-risk-radar/blob/main/dashboard/index.html)**

It shows:
- Overall risk level with visual gauge
- Prioritized risk cards (severity, evidence, recommended action)
- Trend (increasing / stable / decreasing)
- Positive signals & next steps
- Risk breakdown by category

The dashboard loads sample data by default so you can demo it even before the workflow runs.

### Optional: enable permanent GitHub Pages
1. Repo → **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/dashboard`
4. Save — then your dashboard will be at  
   `https://rpriyaprakasm-bit.github.io/ai-project-risk-radar/`

---

## Architecture

```
┌─────────────────────┐
│  Data Collectors    │  ← GitHub (ready) | Jira / Linear / Notion (easy to add)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Risk Analyzer      │  ← Grok (xAI) or Claude
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Report + Dashboard │  ← Markdown Issue + HTML Dashboard + JSON
└─────────────────────┘
```

---

## Quick Start (Grok version — recommended)

1. Go to **Settings → Secrets and variables → Actions**
2. Add secret: `XAI_API_KEY` (get one at [console.x.ai](https://console.x.ai) — **add credits** or the API will return 403)
3. Go to the **Actions** tab → **AI Project Risk Radar (Grok)** → **Run workflow**

That’s it. The workflow will:
- Collect GitHub issues/PRs (or use demo data if the repo is empty)
- Analyze risks with Grok
- Post a Risk Report as a GitHub Issue
- Update the dashboard data

### Claude version (optional)

Add `ANTHROPIC_API_KEY` and run **AI Project Risk Radar (Claude)**.

---

## Project Structure

```text
ai-project-risk-radar/
├── .github/workflows/
│   ├── risk-radar.yml              # Claude version
│   └── risk-radar-grok.yml         # Grok version (recommended)
├── src/
│   ├── collectors/                 # Modular data sources
│   ├── analyzers/
│   │   ├── risk_analyzer.py        # Claude
│   │   └── risk_analyzer_grok.py   # Grok (xAI)
│   └── reporters/
├── dashboard/
│   ├── index.html                  # Interactive Risk Dashboard
│   └── risk_report.json            # Live / sample data
├── prompts/
├── examples/
├── docs/
└── README.md
```

---

## Extending to Jira / Linear / Notion

See [docs/extending.md](docs/extending.md). The collector interface is the same — only the data source changes.

---

## Skills Demonstrated

- Agentic AI system design (Grok + Claude)
- Structured output for dashboards
- Modular, extensible architecture
- GitHub Actions automation
- Real-world Project Management problem solving
- Data visualization (interactive dashboard)

---

## License

MIT

---

**Built to show that AI can do more than generate text — it can actively protect projects.**
