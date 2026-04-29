# Live Provider Smoke Report Contract

Status: DRAFT

Purpose:
- Define the committed, secrets-free report format for verified gated live provider smoke runs.

Report path:
- reports/live_smoke/gated_live_provider_smoke_report.json

Required fields:
- status
- ran_at_utc
- provider_count
- ok_count
- error_count
- has_any_payload
- providers
- execution_side_effects
- secrets_recorded

Rules:
- secrets_recorded must be false.
- execution_side_effects must be false.
- Report must not contain API keys, tokens, raw provider payloads, broker data, IBKR data, orders, or execution intents.
- Provider entries must stay diagnostic-level only: provider_name, status, records_returned, has_error, has_payload.
- Report updates require gated live smoke verification when env is available, plus offline smoke and full test.
