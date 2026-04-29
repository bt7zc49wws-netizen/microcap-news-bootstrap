# Runtime Freshness and Staleness Enforcement Policy

Status: DRAFT

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
