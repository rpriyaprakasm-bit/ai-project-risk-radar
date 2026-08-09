# AI Project Risk Radar

Project risk doesn’t always show up as a red slide. It sits in open issues, quiet blockers, and PRs that never quite land. This repo runs a scheduled pass over work items, scores what looks risky, and drops a report plus a small dashboard.

**Live dashboard:** [open it](https://raw.githack.com/rpriyaprakasm-bit/ai-project-risk-radar/main/docs/index.html)

---

## Flow

1. **Collect** open GitHub issues/PRs (or demo data if the repo is quiet)  
2. **Analyze** with Grok when the key works; if the API fails (no credits, etc.), a rule-based pass still writes a report  
3. **Verify** the JSON before publish — empty or broken reports don’t get committed as success  
4. **Publish** markdown report, optional GitHub Issue, dashboard JSON  

Workflow labels follow that order so a failed step is easy to spot in Actions.

---

## Risk categories I use

Blocker, Schedule, People, Quality, Scope, Communication.

I care more about *kind of problem* than a single red/amber badge. That’s how standups actually talk.

---

## Run it

1. Add `XAI_API_KEY` under **Settings → Secrets → Actions** ([console.x.ai](https://console.x.ai) — needs credits for live Grok)  
2. **Actions → AI Project Risk Radar (Grok) → Run workflow**  
3. Optional: `ANTHROPIC_API_KEY` for the Claude workflow  

Local: `bash scripts/run_demo.sh`

---

## What’s honest about the demo

If there are no open issues, the collector loads sample tickets so the dashboard isn’t blank. That’s deliberate for portfolio viewing. Point it at a busy repo when you want live signal.

When Grok isn’t available, the report is marked as a heuristic fallback — still useful for structure, not the same as a full model pass.

---

## Still on my list

- Jira collector that matches how teams actually label work  
- Noise filter so low-value tickets don’t dominate  
- Trend line across weeks  
- Tighter links from each risk back to the ticket  

---

## Layout

```text
.github/workflows/   schedule + manual
src/collectors/      GitHub first
src/analyzers/       Grok + fallback
src/validators/      report checks before publish
src/reporters/       issue + files
docs/                dashboard
```

More detail on how the steps are wired: [AGENT_LAYERS.md](./AGENT_LAYERS.md)

---

MIT
