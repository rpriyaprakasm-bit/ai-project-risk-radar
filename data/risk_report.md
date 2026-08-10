# Project Risk Report — 2026-08-10

> **Mode:** Local heuristic fallback (xAI team has no credits/licenses (403)).  
> Grok analysis was skipped or unavailable. Add xAI credits to enable AI narrative.

## Overall risk: **Critical**

Local heuristic analysis (xAI team has no credits/licenses (403)). Overall risk Critical from 5 issues and 1 PRs. Top themes: People, Schedule, Scope.

## Risks

### 1. [Critical] Payment gateway integration is blocked by missing API keys
- **Category:** Schedule  
- **Evidence:** Labels: blocker, backend, high-priority. Comments: 8. Due: 2026-07-25. We cannot proceed with the checkout flow until the payment provider gives us production keys. Waiting for 2 weeks already.  
- **Action:** Re-baseline the date past 2026-07-25 or cut scope; name a single accountable owner.

### 2. [Critical] Fix flaky tests in checkout suite
- **Category:** Schedule  
- **Evidence:** Labels: bug, quality. Comments: 12. Due: 2026-07-15. Tests fail randomly on CI. Has been open for a while.  
- **Action:** Re-baseline the date past 2026-07-15 or cut scope; name a single accountable owner.

### 3. [Critical] Critical: Database migration for new order schema
- **Category:** Schedule  
- **Evidence:** Labels: backend, high-priority, database. Comments: 15. Due: 2026-07-20. This is required before we can ship the new order flow. Alice is the only one who knows the old schema.  
- **Action:** Re-baseline the date past 2026-07-20 or cut scope; name a single accountable owner.

### 4. [High] Key-person load on alice
- **Category:** People  
- **Evidence:** alice is assigned to 3 open items.  
- **Action:** Rebalance work away from alice or add backup owners.

### 5. [Medium] Add new discount engine for Black Friday
- **Category:** Scope  
- **Evidence:** Labels: feature, unestimated. Comments: 1. Due: n/a. Marketing wants a completely new discount rules engine. No estimate yet.  
- **Action:** Assign a primary owner and a backup; protect capacity for critical path.

### 6. [Medium] Update user profile page
- **Category:** Scope  
- **Evidence:** Labels: frontend. Comments: 3. Due: n/a. Small UI improvements.  
- **Action:** Track in backlog with next review date.

### 7. [Medium] Long-running WIP PR: WIP: Payment provider sandbox integration
- **Category:** Schedule  
- **Evidence:** Open PR by alice; labels: wip.  
- **Action:** Time-box remaining work or split into reviewable PRs.

## Positive signals

- Some work items are labeled and trackable.
- Delivery activity visible via open pull requests.

## Next steps

1. Address Critical/High items first (blockers and overdue dates).
2. Assign owners where missing on high-severity issues.
3. Add xAI credits at console.x.ai to enable full Grok analysis on the next run.
