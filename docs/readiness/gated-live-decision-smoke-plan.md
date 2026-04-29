# Gated Live Decision Smoke Plan

Status: DRAFT

Purpose:
- Define a gated smoke path for live market/news decision checks without enabling paid APIs, broker integration, IBKR, order generation, or trading execution.

Scope:
- explicit live-smoke gate
- free/live provider calls only when intentionally enabled
- live news plus market data decision check
- no execution side effects
- observable provider and freshness status

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial plan:
- Default behavior remains offline-only.
- Live smoke must require an explicit environment flag.
- Live smoke must print provider status, freshness status, and final canonical decision.
- Live smoke must not generate orders or execution intents.
- Provider failure, rate limit, stale data, or missing data must not silently produce actionable decisions.
- Offline smoke remains the acceptance baseline.
