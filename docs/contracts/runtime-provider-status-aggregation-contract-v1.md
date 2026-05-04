# Runtime Provider Status Aggregation Contract

Status: Accepted Draft

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

Aggregation invariants:
- Empty diagnostic input must return provider_count=0, ok_count=0, error_count=0, has_any_payload=false, latest_fetched_at=null, and providers=[].
- latest_fetched_at must be the maximum fetched_at value from the input diagnostics.
- ok_count and error_count must count diagnostics by status without exceeding provider_count.
- has_any_payload must be true when at least one provider diagnostic has payload.
- providers must preserve input order.

Fixture:
- tests/fixtures/provider_diagnostics/aggregate_provider_status_diagnostics.json
- The aggregation fixture validates stable aggregate output shape without live provider calls.
- Fixture updates require smoke + full test before commit.
