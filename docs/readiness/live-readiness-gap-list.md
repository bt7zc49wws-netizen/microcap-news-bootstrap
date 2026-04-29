# Live Readiness Gap List

Status: DRAFT

Current verified offline baseline:
- full offline decision pipeline smoke ok
- 185 passed
- HEAD: 5130f24

Gaps before live system:
- live provider orchestration policy
- provider failure / fallback behavior
- rate limit and retry policy
- runtime freshness and staleness enforcement
- scheduled ingestion runbook
- live market/news decision smoke with network calls explicitly gated
- no broker, IBKR, order generation, or trading execution until final phase
