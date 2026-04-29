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
- 191 passed
- HEAD: current checkpoint commit

Boundary:
- No paid APIs
- No broker integration
- No IBKR dependency
- No order generation
- No trading execution

Smoke Gates:
- scripts/gated_live_decision_smoke.py requires ENABLE_GATED_LIVE_SMOKE=1.
- scripts/free_provider_smoke.py requires ENABLE_FREE_PROVIDER_SMOKE=1.
- Default mode for both scripts performs no live network calls.

Provider Diagnostics:
- ProviderFetchResult.to_status_diagnostic() is used by gated live smoke for enabled provider fetch status output.
- Raw provider payloads are not dumped by gated live smoke.

Free Provider Diagnostics:
- scripts/free_provider_smoke.py uses ProviderFetchResult.to_status_diagnostic() for enabled provider fetch status output.
- Raw provider payloads are not dumped by free provider smoke.
