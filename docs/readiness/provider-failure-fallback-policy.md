# Provider Failure and Fallback Policy

Status: DRAFT

Purpose:
- Define how provider errors, empty responses, stale responses, malformed payloads, and partial provider outages are handled before live decision usage.

Scope:
- live news provider failures
- live market/fundamental provider failures
- fallback eligibility
- partial accept vs unavailable behavior
- stale data handling hooks

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial policy:
- Provider failures must be explicit and observable.
- Empty or malformed provider responses must not silently produce actionable decisions.
- Fallback providers may be used only when freshness and source attribution remain clear.
- If required live inputs are unavailable, the decision path must degrade to no_trade or unavailable status.
- A fallback result must carry source trace metadata.
- Retrying and rate-limit behavior are governed separately by the rate limit and retry policy.
