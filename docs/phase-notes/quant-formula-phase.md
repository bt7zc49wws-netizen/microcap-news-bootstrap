# Quant Formula Phase

Status: DONE

Scope completed:
- API-independent pure formula layer
- price_change_pct
- gap_pct
- intraday_return_pct
- relative_volume
- dollar_volume
- range_pct
- close_location_value
- VWAP
- VWAP distance %
- true range
- ATR
- ATR %
- breakout %
- slope
- acceleration
- smoke script

Rules preserved:
- no paid API
- no trading execution
- no IBKR
- pure functions only
- tests green before commit
- current architecture preserved

Latest validation:
- quant formula smoke ok
- 125 passed


Contract:
- docs/contracts/quant-signal-contract-v1.md


Signal Builder Extension:
- Status: ACTIVE_DRAFT
- src/app/quant/signals.py
- tests/quant/test_signals.py
- scripts/quant/smoke_quant_signal_builder.py
- build_quant_signal creates canonical quant signal output from validated market snapshot values.


Decision Context Extension:
- Status: DRAFT
- src/app/decision_context.py
- tests/test_decision_context.py
- scripts/quant/smoke_decision_context_builder.py
- docs/contracts/decision-context-contract-v1.md
- build_decision_context combines already-computed news and quant inputs.


Decision Engine Extension:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- scripts/quant/smoke_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- make_decision_result creates canonical no_trade/watchlist/actionable result shape.


Decision Evaluator Extension:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- scripts/quant/smoke_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- evaluate_decision_context applies initial deterministic offline-safe rules.


Supported News Event Gate:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- scripts/quant/smoke_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- Supported event types now gate decision evaluation before quant confirmation.


Decision Threshold Defaults:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- DEFAULT_DECISION_THRESHOLDS now owns strong quant confirmation thresholds.


Decision Reason Code Registry:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- VALID_REASON_CODES now owns evaluator-facing reason code identifiers.


Decision Result Symbol Trace:
- Status: DRAFT
- src/app/decision_engine.py
- tests/test_decision_engine.py
- scripts/quant/smoke_decision_engine.py
- docs/contracts/decision-engine-contract-v1.md
- Decision results can now carry uppercase symbol trace for API/dashboard/replay observability.


Decision Result Schema Hardening:
- Status: DRAFT
- docs/contracts/decision-engine-contract-v1.md
- Required fields: decision, reason_codes
- Optional fields: symbol
- Timestamp, score, execution, and order fields are intentionally excluded from this offline-safe phase.


News Decision Adapter Extension:
- Status: DRAFT
- src/app/news_decision_adapter.py
- tests/test_news_decision_adapter.py
- scripts/quant/smoke_news_decision_adapter.py
- docs/contracts/news-decision-adapter-contract-v1.md
- adapt_news_for_decision maps classification output into decision-context news input.


News To Decision E2E Path:
- Status: DRAFT
- scripts/quant/smoke_news_to_decision.py
- docs/contracts/news-decision-adapter-contract-v1.md
- Offline chain now validates classification output → decision-context news input → decision context → canonical decision result.


Full Offline Decision Pipeline Smoke:
- Status: DRAFT
- scripts/quant/smoke_full_offline_decision_pipeline.py
- Offline chain now validates Stooq OHLCV rows → enrichment → market snapshot adapter → quant signal → classification output → news decision adapter → decision context → canonical decision result.
- No live provider, paid API, broker, IBKR, trading execution, or order generation is used.


Full Offline Decision Pipeline Closure:
- Status: LOCKED for offline smoke coverage
- Final smoke: scripts/quant/smoke_full_offline_decision_pipeline.py
- Contract reference: docs/contracts/news-decision-adapter-contract-v1.md
- Last verified:
  - full offline decision pipeline smoke ok
  - 184 passed
- This closes the offline-safe Stooq OHLCV → quant signal → classification → news adapter → decision context → canonical decision result path.
- Live providers, paid APIs, broker, IBKR, trading execution, and order generation remain explicitly out of scope for this phase.


Decision Context Audit Trace:
- Status: LOCKED
- `build_decision_context` now supports optional non-empty `audit_trace`.
- Full offline decision smoke now passes audit trace through the Stooq → quant → classification → news adapter → decision context → decision result path.
- Audit trace remains offline-safe and must not introduce live provider calls, paid APIs, broker, IBKR, order generation, or trading execution.
- Last verified:
  - full offline decision pipeline smoke ok
  - 185 passed


Offline Decision Result Fixture:
- Status: LOCKED
- Fixture: tests/fixtures/offline_decision/full_offline_decision_result.json
- Full offline decision smoke now validates the canonical decision result against a committed fixture snapshot.
- Last verified:
  - full offline decision pipeline smoke ok
  - 185 passed


Live Readiness Draft Set:
- Status: DRAFT SET COMPLETE
- Policy index: docs/readiness/live-readiness-policy-index.md
- Gap list: docs/readiness/live-readiness-gap-list.md
- Policies drafted:
  - live provider orchestration
  - provider failure / fallback behavior
  - rate limit and retry policy
  - runtime freshness and staleness enforcement
  - scheduled ingestion runbook
  - gated live decision smoke plan
  - execution boundary policy
- Last verified:
  - full offline decision pipeline smoke ok
  - 185 passed


Live Readiness Policy Index:
- Status: Accepted Draft
- Index: docs/readiness/live-readiness-policy-index.md
- Last verified:
  - full offline decision pipeline smoke ok
  - 185 passed


Live Readiness Accepted Draft Closure:
- Status: Accepted Draft
- Report: reports/readiness/live_readiness_checkpoint_report.json
- Policy index: docs/readiness/live-readiness-policy-index.md
- Moving HEAD pinning removed; readiness docs now use current checkpoint commit wording.
- Last verified:
  - full offline decision pipeline smoke ok
  - 185 passed


Gated Live Decision Smoke:
- Status: DRAFT IMPLEMENTED
- Script: scripts/gated_live_decision_smoke.py
- Default behavior: skipped unless ENABLE_GATED_LIVE_SMOKE=1 is set.
- Verified default mode:
  - no live network calls
  - no broker
  - no IBKR
  - no order generation
  - no trading execution
  - no decision context build
  - no evaluate_decision_context call
  - no canonical decision result output
- Last verified:
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 185 passed


Gated Live Smoke Boundary Closure:
- Status: LOCKED
- Script: scripts/gated_live_decision_smoke.py
- Default mode remains skip unless ENABLE_GATED_LIVE_SMOKE=1 is set.
- Boundary locked:
  - provider fetch checks only
  - no decision context build
  - no evaluate_decision_context call
  - no canonical decision result output
  - no broker, IBKR, order generation, or trading execution
- Last verified:
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 185 passed


Free Provider Smoke Gate:
- Status: LOCKED
- Script: scripts/free_provider_smoke.py
- Default behavior: skipped unless ENABLE_FREE_PROVIDER_SMOKE=1 is set.
- Verified default mode:
  - no live network calls
  - no broker
  - no IBKR
  - no order generation
  - no trading execution
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 185 passed


Smoke Script Gate Tests:
- Status: LOCKED
- Test: tests/test_smoke_script_gates.py
- Verifies default skip behavior for:
  - scripts/free_provider_smoke.py
  - scripts/gated_live_decision_smoke.py
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 187 passed


Enabled Smoke Env Guard:
- Status: LOCKED
- scripts/free_provider_smoke.py skips when ENABLE_FREE_PROVIDER_SMOKE=1 but FINNHUB_API_KEY is missing.
- scripts/gated_live_decision_smoke.py skips when ENABLE_GATED_LIVE_SMOKE=1 but FINNHUB_API_KEY is missing.
- This prevents accidental live network calls with incomplete provider config.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 189 passed


Provider Fetch Status Diagnostic:
- Status: LOCKED
- ProviderFetchResult now exposes to_status_diagnostic().
- Diagnostic includes provider_name, status, records_returned, fetched_at, has_error, and optional error_message.
- This supports live provider fetch status reporting without broker, IBKR, order generation, or trading execution.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 190 passed


Provider Diagnostics Readiness Index:
- Status: LOCKED
- Index updated: docs/readiness/live-readiness-policy-index.md
- Gated live smoke uses ProviderFetchResult.to_status_diagnostic() for enabled provider fetch status output.
- Raw provider payloads are not dumped by gated live smoke.
- Last verified:
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 190 passed


Provider Diagnostics Payload Presence:
- Status: LOCKED
- ProviderFetchResult.to_status_diagnostic() now includes has_payload.
- This allows gated live smoke diagnostics to report payload presence without dumping raw payloads.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 191 passed


Free Provider Diagnostics Readiness Index:
- Status: LOCKED
- Index updated: docs/readiness/live-readiness-policy-index.md
- Free provider smoke uses ProviderFetchResult.to_status_diagnostic() for enabled provider fetch status output.
- Raw provider payloads are not dumped by free provider smoke.
- Last verified:
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 191 passed


Provider Diagnostics JSON Serialization:
- Status: LOCKED
- Test: tests/services/providers/test_provider_types.py
- ProviderFetchResult.to_status_diagnostic() is verified as JSON-serializable.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Status Endpoint Contract Test:
- Status: LOCKED
- Test: tests/test_status_endpoint.py
- Validates /api/v1/status freshness contract shape.
- Checks overall_status, is_stale, freshness_threshold_seconds, and dependencies.read_model.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Status Endpoint Contract Strengthening:
- Status: LOCKED
- Test: tests/test_status_endpoint.py
- /api/v1/status now verifies freshness timestamps and meta fields in addition to freshness/status shape.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Status Degraded With Healthy Read Model:
- Status: LOCKED
- Test: tests/test_status_endpoint.py
- /api/v1/status explicitly asserts overall_status=degraded while dependencies.read_model=ok when data is stale.
- This confirms freshness degradation is separate from read-model availability.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Provider Diagnostics Status Boundary:
- Status: LOCKED
- ProviderFetchResult.to_status_diagnostic() remains provider-fetch scoped.
- /api/v1/status remains runtime/read-model scoped.
- Provider diagnostics are not copied into /api/v1/status unless a dedicated runtime aggregation contract is added.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Runtime Freshness Policy Accepted Draft:
- Status: Accepted Draft
- Policy: docs/readiness/runtime-freshness-staleness-policy.md
- Confirms stale runtime data can degrade /api/v1/status while dependencies.read_model remains ok.
- Provider diagnostics remain provider-fetch scoped and are not copied into /api/v1/status.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Provider Tests Offline Safety:
- Status: LOCKED
- Tests updated:
  - tests/services/providers/fundamentals/test_fundamentals_client.py
  - tests/services/providers/sec_edgar/test_sec_edgar_client.py
- Provider unit tests now monkeypatch network calls and do not depend on live DNS/provider availability.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed
