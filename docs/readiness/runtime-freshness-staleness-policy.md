# Runtime Freshness and Staleness Enforcement Policy

Status: Accepted Draft

Purpose:
- Define how runtime data freshness and stale input handling must work before live decision usage.

Scope:
- live news freshness
- live market/fundamental freshness
- stale input detection
- freshness thresholds
- degraded/unavailable runtime states
- decision gating from stale inputs

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial policy:
- Runtime decisions must evaluate input freshness before producing an actionable result.
- Freshness thresholds must be explicit and configurable.
- Stale required inputs must not silently produce actionable decisions.
- If required inputs are stale, runtime behavior must degrade to no_trade, degraded, or unavailable according to API/readiness contracts.
- Freshness evaluation timestamps must be observable.
- Offline decision smoke remains the baseline and must not depend on live freshness checks.

Runtime status observation:
- /api/v1/status returns degraded when current read-model data is stale.
- Stale status is represented by is_stale=true while dependencies.read_model can remain ok.
- This separates data freshness degradation from read model availability.

Provider diagnostics boundary:
- ProviderFetchResult.to_status_diagnostic() is provider-fetch scoped.
- /api/v1/status remains runtime/read-model scoped.
- Provider diagnostics must not be copied into /api/v1/status unless a dedicated runtime aggregation contract is added.
- Current /api/v1/status freshness behavior remains based on read-model/job freshness and dependency availability.
