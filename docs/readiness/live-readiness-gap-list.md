# Live Readiness Gap List

Status: DRAFT

Current verified offline baseline:
- full offline decision pipeline smoke ok
- 185 passed
- HEAD: 319ccb3

Gaps before live system:
- live provider orchestration policy — DRAFT ADDED: docs/readiness/live-provider-orchestration-policy.md
- provider failure / fallback behavior — DRAFT ADDED: docs/readiness/provider-failure-fallback-policy.md
- rate limit and retry policy — DRAFT ADDED: docs/readiness/rate-limit-retry-policy.md
- runtime freshness and staleness enforcement
- scheduled ingestion runbook
- live market/news decision smoke with network calls explicitly gated
- no broker, IBKR, order generation, or trading execution until final phase
