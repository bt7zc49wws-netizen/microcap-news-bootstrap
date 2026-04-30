# Live Smoke Environment Readiness Checklist

Status: Accepted Draft

Before enabling gated live smoke:
- FINNHUB_API_KEY is set.
- SEC_EDGAR_USER_AGENT is set to a real contact string.
- ENABLE_GATED_LIVE_SMOKE=1 is explicitly set only for the live smoke run.
- GATED_LIVE_SMOKE_SYMBOL is set or defaults intentionally to AAPL.
- GATED_LIVE_SMOKE_CIK is set or defaults intentionally to 0000320193.

Safety checks:
- Free provider smoke remains disabled unless ENABLE_FREE_PROVIDER_SMOKE=1 is explicitly set.
- Gated live smoke must print provider diagnostics and aggregate diagnostics only.
- Gated live smoke writes reports/live_smoke/gated_live_provider_smoke_report.json using the accepted report contract.
- No decision context build.
- No evaluate_decision_context call.
- No canonical decision result output.
- No broker, IBKR, order generation, or trading execution.

Example live smoke command:
```bash
export FINNHUB_API_KEY="..."
export SEC_EDGAR_USER_AGENT="name email@example.com"
export ENABLE_GATED_LIVE_SMOKE=1
python scripts/gated_live_decision_smoke.py
unset ENABLE_GATED_LIVE_SMOKE
python -m pytest tests/test_live_provider_smoke_report_contract.py
```
