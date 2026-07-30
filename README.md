# AI Project Risk Radar

**Early-warning risk visibility for project and operations teams — automated with AI.**

In business operations and delivery work, risks rarely fail loudly on day one. They sit in tickets, inboxes, and status decks until they cost a sprint, a release, or a stakeholder conversation.

This project is a practical example of using AI to support **operations control**: pull signal from work tracking data, surface what matters, and put it in a dashboard leadership can scan in minutes — not another manual RAID scrub.

Built as a hands-on automation pattern using **Grok** (with optional Claude), GitHub Actions, and a simple HTML dashboard.

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Grok](https://img.shields.io/badge/Powered%20by-Grok-000000?logo=x&logoColor=white)](https://x.ai)
[![Dashboard](https://img.shields.io/badge/Live-Dashboard-38bdf8)](https://raw.githack.com/rpriyaprakasm-bit/ai-project-risk-radar/main/docs/index.html)

---

## Why this exists (operations lens)

Typical ops / PMO pain:

- Blockers age quietly while status reports stay “green”
- Risk logs are updated late or inconsistently
- Leadership asks for a clear view; teams spend hours assembling it by hand

**Risk Radar** automates the first pass:

1. Collect open work items (GitHub issues/PRs today; Jira-style sources are the natural extension)
2. Analyze with an LLM against a fixed risk framework
3. Publish a structured report + visual dashboard (by category, severity, and recommended action)

It is not a full PPM tool. It is an **AI-assisted control layer** — the same idea you would apply inside a Business Operations team or an AI Value Hub delivery pipeline.

---

## Dashboard

![Dashboard snapshot](docs/dashboard-preview.svg)

**Live demo:** [Open interactive dashboard](https://raw.githack.com/rpriyaprakasm-bit/ai-project-risk-radar/main/docs/index.html)

(Permanent GitHub Pages URL, once enabled: `https://rpriyaprakasm-bit.github.io/ai-project-risk-radar/`)

**What you see:**
- Category tiles (Blocker, Schedule, People, Quality, Scope, Communication)
- Distribution and count charts
- Overall risk level and summary for leadership scan
- Risk cards grouped by category, with evidence and suggested actions

---

## What it does

| Step | Output |
|------|--------|
| Collect | Open issues/PRs (or demo data for a reliable portfolio run) |
| Analyze | Grok or Claude scores risks using a defined category model |
| Report | Markdown risk report + GitHub Issue |
| Visualize | HTML dashboard + JSON for reuse in other tools |

### Risk categories

| Category | What it flags |
|----------|----------------|
| **Blocker** | Stuck work, external dependencies, waiting-on items |
| **Schedule** | Missed dates, overload, slip patterns |
| **People** | Bus factor, coverage gaps, access delays |
| **Quality** | Defect/test noise, error spikes |
| **Scope** | Unestimated or late-breaking work |
| **Communication** | Stale updates, silent critical items |

Category-first layout was chosen on purpose: in standups and ops reviews, people ask *what kind of problem is this?* before *how red is the badge?*

---

## How this maps to real roles

**Business Operations / Program Ops**  
Automated risk scan + dashboard = less manual status assembly, earlier escalation, clearer ownership.

**AI Value Hub / AI Enablement**  
Example of a governed automation pattern: fixed intake of data → structured AI analysis → human-readable output → visible metrics. Useful as a template for other “scan → summarize → act” use cases (status packs, intake triage, meeting actions).

**Tools demonstrated:** GitHub Actions, Grok, Claude, structured prompting, JSON + dashboard reporting — aligned with multi-LLM and automation work (Power Automate / n8n-style thinking, implemented here as code automation for a clean public demo).

---

## Quick start

### Grok (default)

1. **Settings → Secrets → Actions** → add `XAI_API_KEY` ([console.x.ai](https://console.x.ai); credits required)
2. **Actions → AI Project Risk Radar (Grok) → Run workflow**

### Claude (optional)

Add `ANTHROPIC_API_KEY` and run the Claude workflow.

### Dashboard hosting

1. **Settings → Pages → Source → GitHub Actions**
2. Run **Deploy Dashboard** (or push to `main`)

---

## Demo vs live data

The dashboard includes **sample risks** so the demo is always populated for portfolio review. When the workflow runs against a repo with real issues, analysis can replace that sample set.

---

## Roadmap

- [ ] Jira (or similar) collector for enterprise work tracking
- [ ] Noise filters so low-value tickets do not dominate the view
- [ ] Trend across runs (is overall risk rising or falling?)
- [ ] Alert when overall risk moves to Critical
- [ ] Tighter evidence links back to ticket IDs

---

## Repo layout

```text
.github/workflows/   Scheduled + manual runs (Grok / Claude / Pages)
src/collectors/      Data sources (GitHub first; others stubbed)
src/analyzers/       LLM analysis + structured output
src/reporters/       Issue + JSON publishing
docs/                Dashboard, snapshot, sample report data
prompts/             Prompt templates
```

---

## Design choices

- **AI for the first pass, humans for decisions** — the tool ranks and explains; owners still act.
- **Category model over severity-only** — easier to assign and discuss in ops forums.
- **Reusable pattern** — same flow supports status digests, intake scoring, or action extraction with different prompts and sources.

---

## License

MIT
