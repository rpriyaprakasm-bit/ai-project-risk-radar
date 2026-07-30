# Project Risk Report
**Date:** 2026-07-30
**Overall Risk Level:** High
**Summary:** The project has several concentrated risks around a single engineer and a long-running blocker that is already past its due date. Scope is also expanding without estimates.

## Top Risks

### 1. Critical work is concentrated on a single person
- **Category:** People
- **Severity:** High
- **Confidence:** High
- **Evidence:** Alice is the only assignee on #29 (critical database migration), #42 (payment blocker), and #55. She also has the only open PR related to payments.
- **Recommended Action:** Immediately pair or reassign at least one of the high-priority items. Document the database schema knowledge.

### 2. Payment integration blocked for more than 2 weeks
- **Category:** Blocker
- **Severity:** High
- **Confidence:** High
- **Evidence:** Issue #42 has label `blocker`, was created 20 days ago, due date was 2026-07-25 (already missed), and has 8 comments still waiting on external API keys.
- **Recommended Action:** Escalate to the payment provider or prepare a temporary mock/fallback path so other work is not blocked.

### 3. New high-impact feature added without estimate
- **Category:** Scope
- **Severity:** Medium
- **Confidence:** Medium
- **Evidence:** Issue #51 ("Add new discount engine for Black Friday") was created 3 days ago with label `unestimated` and no assignee.
- **Recommended Action:** Run a quick estimation session and decide whether this belongs in the current release.

### 4. Long-lived quality issue
- **Category:** Quality
- **Severity:** Medium
- **Confidence:** Medium
- **Evidence:** Issue #38 (flaky checkout tests) has been open for 25 days, is past its due date, and has 12 comments.
- **Recommended Action:** Schedule a focused bug-bash or quarantine the flaky tests so they stop eroding confidence in CI.

## Positive Signals
- There is active recent work (several issues updated in the last few days).
- Most issues have clear labels.

## Trend
Risk appears to be **increasing** because a critical blocker has already missed its deadline and key knowledge remains siloed.

## Suggested Next Steps
1. Unblock or escalate the payment gateway issue this week.
2. Reduce bus-factor risk on Alice’s critical tasks.
3. Estimate and prioritize (or defer) the new discount engine request.
