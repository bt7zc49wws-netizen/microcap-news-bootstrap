# Live Readiness Policy Index

Status: Accepted Draft

Policies:
- docs/readiness/live-provider-orchestration-policy.md
- docs/readiness/provider-failure-fallback-policy.md
- docs/readiness/rate-limit-retry-policy.md
- docs/readiness/runtime-freshness-staleness-policy.md
- docs/readiness/scheduled-ingestion-runbook.md
- docs/readiness/gated-live-decision-smoke-plan.md
- docs/readiness/execution-boundary-policy.md

Baseline:
- full offline decision pipeline smoke ok
- 185 passed
- HEAD: b6fa75b

Boundary:
- No paid APIs
- No broker integration
- No IBKR dependency
- No order generation
- No trading execution
