# Smoke Environment Contract

Status: DRAFT

Required gates:
- ENABLE_FREE_PROVIDER_SMOKE=1 is required to run scripts/free_provider_smoke.py with live provider calls.
- ENABLE_GATED_LIVE_SMOKE=1 is required to run scripts/gated_live_decision_smoke.py with live provider calls.

Required provider config when enabled:
- FINNHUB_API_KEY must be set before either live smoke can fetch provider data.
- SEC_EDGAR_USER_AGENT should be set for SEC EDGAR calls; default test@example.com is allowed only for local smoke scaffolding.

Default behavior:
- If gate env is missing, smoke scripts must skip without live network calls.
- If gate env is enabled but FINNHUB_API_KEY is missing, smoke scripts must skip before provider fetch or aggregation.

Execution boundary:
- No broker calls.
- No IBKR calls.
- No order generation.
- No trading execution.
