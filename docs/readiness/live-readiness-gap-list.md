# Live Readiness Gap List

Status: DRAFT

Current verified offline baseline:
- full offline decision pipeline smoke ok
- 185 passed
- HEAD: b6fa75b

Gaps before live system:
- live provider orchestration policy — DRAFT ADDED: docs/readiness/live-provider-orchestration-policy.md
- provider failure / fallback behavior — DRAFT ADDED: docs/readiness/provider-failure-fallback-policy.md
- rate limit and retry policy — DRAFT ADDED: docs/readiness/rate-limit-retry-policy.md
- runtime freshness and staleness enforcement — DRAFT ADDED: docs/readiness/runtime-freshness-staleness-policy.md
- scheduled ingestion runbook — DRAFT ADDED: docs/readiness/scheduled-ingestion-runbook.md
- live market/news decision smoke with network calls explicitly gated — DRAFT ADDED: docs/readiness/gated-live-decision-smoke-plan.md
- no broker, IBKR, order generation, or trading execution until final phase — DRAFT ADDED: docs/readiness/execution-boundary-policy.md
