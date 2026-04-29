# Live Provider Orchestration Policy

Status: DRAFT

Purpose:
- Define how live/free providers will be orchestrated before any paid API, broker, IBKR, order generation, or trading execution work begins.

Scope:
- live news provider calls
- live market/fundamental provider calls
- provider selection order
- provider failure handling hooks
- freshness and staleness hooks

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial policy:
- Offline decision pipeline remains the baseline acceptance path.
- Live provider orchestration must be explicitly gated.
- Provider calls must be observable, bounded, and retry-limited.
- Provider failures must not silently produce actionable decisions.
- Missing or stale live data must degrade to no_trade or unavailable status, not execution behavior.
