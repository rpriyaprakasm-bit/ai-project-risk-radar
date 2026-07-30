# Limitations

Written so future-me (and anyone forking this) doesn’t assume magic.

## Data source

- Only the **GitHub collector** is implemented.
- Jira / Linear / Notion folders exist as placeholders. The interface is intentional; the HTTP clients are not.
- Private repos need a token with `repo` scope. Fine-grained tokens work if issues + PRs are allowed.

## Model behavior

- Risk ranking depends on the model and the prompt. Same board can get slightly different severity calls across runs.
- Long comment threads get truncated before analysis. Deep archaeology isn’t the goal — early signals are.
- The model has no Slack / meeting context. If the “real” blocker only lives in a call, this won’t see it.

## Auth & cost

- Grok path needs `XAI_API_KEY` **with credits**. A zero-balance key fails with 403.
- Claude path needs `ANTHROPIC_API_KEY`.
- I didn’t add spend caps or caching. Don’t point this at a huge org without limits.

## Dashboard

- Regenerated on each successful workflow run (or from embedded demo data).
- No login, no per-user views, no historical compare UI yet.
- Category charts were preferred over severity-only after trying both; severity is still on each card.

## Ops

- GitHub Pages must be switched to **GitHub Actions** source once by a human in Settings.
- Node / action version pins will age; expect to bump `actions/checkout` etc. over time.

## What I would not claim

- This does not replace a PM or a risk register.
- This does not “guarantee” on-time delivery.
- This is an assistant for scanning, not an automated decision maker.
