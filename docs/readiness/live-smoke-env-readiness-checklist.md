# Live Smoke Environment Readiness Checklist

Status: DRAFT

Before enabling gated live smoke:
- FINNHUB_API_KEY is set.
- SEC_EDGAR_USER_AGENT is set to a real contact string.
- ENABLE_GATED_LIVE_SMOKE=1 is explicitly set only for the live smoke run.
- GATED_LIVE_SMOKE_SYMBOL is set or defaults intentionally to AAPL.
- GATED_LIVE_SMOKE_CIK is set or defaults intentionally to 0000320193.

Safety checks:
- Free provider smoke remains disabled unless ENABLE_FREE_PROVIDER_SMOKE=1 is explicitly set.
- Gated live smoke must print provider diagnostics and aggregate diagnostics only.
- No decision context build.
- No evaluate_decision_context call.
- No canonical decision result output.
- No broker, IBKR, order generation, or trading execution.
