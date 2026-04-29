# Rate Limit and Retry Policy

Status: DRAFT

Purpose:
- Define bounded retry behavior, timeout handling, and rate-limit response handling before live provider usage.

Scope:
- live news provider calls
- live market/fundamental provider calls
- retry limits
- timeout limits
- rate-limit handling
- backoff hooks

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial policy:
- Provider calls must have explicit timeout limits.
- Retries must be bounded and observable.
- Rate-limit responses must not silently produce actionable decisions.
- Exhausted retries must degrade to unavailable, stale, or no_trade behavior according to provider failure policy.
- Retry metadata must be traceable in runtime logs or audit fields.
- No retry loop may block the offline decision baseline.
