# Runtime Provider Status Aggregation Contract

Status: DRAFT

Purpose:
- Define a future-safe boundary for aggregating provider fetch diagnostics without copying them directly into /api/v1/status.

Inputs:
- ProviderFetchResult.to_status_diagnostic() outputs from enabled provider fetches.

Rules:
- Provider diagnostics are provider-fetch scoped.
- /api/v1/status remains runtime/read-model scoped.
- Aggregated provider status must be exposed through a dedicated future surface, not silently merged into /api/v1/status.
- Aggregation must remain read-only and must not generate orders, execution intents, broker calls, or IBKR calls.
- Missing provider diagnostics must degrade status visibility, not trigger execution behavior.

Minimum aggregate fields:
- provider_count
- ok_count
- error_count
- has_any_payload
- latest_fetched_at
- providers
