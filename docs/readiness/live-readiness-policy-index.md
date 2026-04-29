# Live Readiness Policy Index

Status: Accepted Draft

Policies:
- docs/readiness/live-provider-orchestration-policy.md
- docs/readiness/provider-failure-fallback-policy.md
- docs/readiness/rate-limit-retry-policy.md
- docs/readiness/runtime-freshness-staleness-policy.md — Accepted Draft
- docs/readiness/scheduled-ingestion-runbook.md
- docs/readiness/gated-live-decision-smoke-plan.md
- docs/readiness/execution-boundary-policy.md

Baseline:
- full offline decision pipeline smoke ok
- 197 passed
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

Runtime Status Observation:
- /api/v1/status returns degraded when read-model data is stale while dependencies.read_model can remain ok.
- This separates freshness degradation from read model availability.

Provider Aggregation:
- docs/contracts/runtime-provider-status-aggregation-contract-v1.md — Accepted Draft

Smoke Environment Contract:
- docs/readiness/smoke-environment-contract.md
- Defines ENABLE_FREE_PROVIDER_SMOKE, ENABLE_GATED_LIVE_SMOKE, FINNHUB_API_KEY, and SEC_EDGAR_USER_AGENT expectations.
- Confirms default skip behavior and execution boundary.

Live Smoke Environment Readiness Checklist:
- docs/readiness/live-smoke-env-readiness-checklist.md
- Defines required env values before enabling gated live smoke.
- Confirms no decision context, no evaluate_decision_context, no canonical decision result, no broker, no IBKR, no order generation, and no trading execution.

Verified Live Provider Smoke:
- Report: reports/live_smoke/gated_live_provider_smoke_report.json
- Provider aggregate: provider_count=4, ok_count=4, error_count=0, has_any_payload=true.
- Secrets recorded: false.
- Execution side effects: false.

Live Provider Smoke Report Contract:
- docs/contracts/live-provider-smoke-report-contract-v1.md
- Report path: reports/live_smoke/gated_live_provider_smoke_report.json
- Contract requires secrets_recorded=false and execution_side_effects=false.
