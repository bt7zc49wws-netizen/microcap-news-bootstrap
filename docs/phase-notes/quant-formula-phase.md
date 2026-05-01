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


Runtime Provider Status Aggregation Contract:
- Status: DRAFT
- Contract: docs/contracts/runtime-provider-status-aggregation-contract-v1.md
- Defines future-safe provider diagnostics aggregation boundary without copying diagnostics directly into /api/v1/status.
- Aggregation remains read-only and must not generate execution intents, broker calls, IBKR calls, or orders.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 193 passed


Provider Status Diagnostics Aggregation:
- Status: LOCKED
- Code: src/app/services/providers/diagnostics.py
- Test: tests/services/providers/test_provider_diagnostics.py
- Aggregates provider_count, ok_count, error_count, has_any_payload, latest_fetched_at, and providers.
- Keeps provider diagnostics separate from /api/v1/status.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 194 passed


Provider Aggregation Contract Accepted Draft:
- Status: Accepted Draft
- Contract: docs/contracts/runtime-provider-status-aggregation-contract-v1.md
- Code: src/app/services/providers/diagnostics.py
- Test: tests/services/providers/test_provider_diagnostics.py
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 194 passed


Gated Live Smoke Aggregation Output:
- Status: LOCKED
- Script: scripts/gated_live_decision_smoke.py
- Gated live smoke now prints individual provider diagnostics plus aggregate_provider_status_diagnostics(diagnostics).
- Aggregate output includes provider_count, ok_count, error_count, has_any_payload, latest_fetched_at, and providers.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 194 passed


Gated Smoke Aggregation Guard:
- Status: LOCKED
- Test: tests/test_smoke_script_gates.py
- When ENABLE_GATED_LIVE_SMOKE=1 but FINNHUB_API_KEY is missing, gated live smoke skips before provider aggregation.
- The skip output must not include provider_count.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 194 passed


Provider Aggregation Fixture:
- Status: LOCKED
- Fixture: tests/fixtures/provider_diagnostics/aggregate_provider_status_diagnostics.json
- Test: tests/services/providers/test_provider_diagnostics.py
- Validates aggregate_provider_status_diagnostics against a committed fixture.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 195 passed


Live Smoke Environment Readiness Checklist:
- Status: LOCKED
- Checklist: docs/readiness/live-smoke-env-readiness-checklist.md
- Defines required env values before enabling gated live smoke.
- Confirms no decision context, no evaluate_decision_context, no canonical decision result, no broker, no IBKR, no order generation, and no trading execution.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 195 passed


Smoke Environment Readiness Accepted Draft:
- Status: Accepted Draft
- Checklist: docs/readiness/live-smoke-env-readiness-checklist.md
- Contract: docs/readiness/smoke-environment-contract.md
- Live smoke remains disabled unless explicit env gates and required provider config are set.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 195 passed


Gated Live Smoke SEC User-Agent Guard:
- Status: LOCKED
- Script: scripts/gated_live_decision_smoke.py
- Test: tests/test_smoke_script_gates.py
- When ENABLE_GATED_LIVE_SMOKE=1, SEC_EDGAR_USER_AGENT must be set and must not be test@example.com.
- Missing/default SEC user-agent skips before provider fetch or aggregation.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 197 passed


Gated Live Provider Smoke Verified:
- Status: VERIFIED
- Report: reports/live_smoke/gated_live_provider_smoke_report.json
- Live provider aggregate result: provider_count=4, ok_count=4, error_count=0, has_any_payload=true.
- Verified providers: finnhub, sec_edgar, market_data, fundamentals.
- Execution side effects: false.
- Secrets recorded: false.
- Last verified:
  - gated live provider smoke completed without execution side effects
  - full offline decision pipeline smoke ok
  - 197 passed


Live Provider Smoke Report Contract:
- Status: DRAFT
- Contract: docs/contracts/live-provider-smoke-report-contract-v1.md
- Report: reports/live_smoke/gated_live_provider_smoke_report.json
- Defines committed, secrets-free report format for verified gated live provider smoke runs.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 197 passed


Live Provider Smoke Report Contract Accepted Draft:
- Status: Accepted Draft
- Contract: docs/contracts/live-provider-smoke-report-contract-v1.md
- Report: reports/live_smoke/gated_live_provider_smoke_report.json
- Secrets recorded must remain false.
- Execution side effects must remain false.
- Last verified:
  - free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set
  - gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set
  - full offline decision pipeline smoke ok
  - 197 passed

Live Provider Smoke Report Implementation Closed:
- Status: IMPLEMENTED
- Script: scripts/gated_live_decision_smoke.py
- Builder: src/app/services/providers/diagnostics.py
- Contract test: tests/test_live_provider_smoke_report_contract.py
- Readiness checklist: docs/readiness/live-smoke-env-readiness-checklist.md
- Gated live smoke now writes the accepted report format without secrets or execution side effects.
- Last verified:
  - contract test passed: 2 passed
  - full test suite passed: 200 passed

Live Smoke Report Readiness Closed:
- Status: IMPLEMENTED
- Validator: src/app/services/providers/live_smoke_report_readiness.py
- CLI check: scripts/check_live_smoke_report_readiness.py
- Tests: tests/services/providers/test_live_smoke_report_readiness.py, tests/test_live_smoke_report_readiness_script.py
- Readiness checklist: docs/readiness/live-smoke-env-readiness-checklist.md
- Report readiness can now be checked with python scripts/check_live_smoke_report_readiness.py.
- Last verified:
  - readiness CLI returned ok
  - full test suite passed: 204 passed

Quant Field Guards Closed:
- Status: IMPLEMENTED
- Signal fields constant: src/app/quant/signals.py::QUANT_SIGNAL_FIELDS
- Enriched payload fields constant: src/app/quant/enrichment.py::ENRICHED_MARKET_PAYLOAD_FIELDS
- Guards: build_quant_signal and enrich_stooq_market_payload raise ValueError on field drift.
- Contract: docs/contracts/quant-signal-contract-v1.md
- Last verified:
  - quant signal/enrichment guard tests passed: 26 passed
  - full test suite passed: 207 passed

Decision Quant Signal Guard Closed:
- Status: IMPLEMENTED
- Decision context guard: src/app/decision_context.py rejects non-canonical quant_signal fields.
- Decision engine tests use src/app/quant/signals.py::QUANT_SIGNAL_FIELDS-shaped helper payloads.
- Last verified:
  - decision context tests passed: 6 passed
  - decision engine tests passed: 16 passed
  - full test suite passed: 208 passed

Decision Threshold Boundary Closed:
- Status: IMPLEMENTED
- Test: tests/test_decision_engine.py::test_evaluate_decision_context_uses_default_threshold_boundaries
- DEFAULT_DECISION_THRESHOLDS is now covered at the actionable boundary for price_change_pct and relative_volume.
- Last verified:
  - decision engine tests passed: 17 passed
  - full test suite passed: 209 passed

Quant Decision Guard Joint Verification:
- Status: VERIFIED
- Scope: tests/quant, tests/test_decision_context.py, tests/test_decision_engine.py
- Last verified:
  - quant + decision guard suite passed: 88 passed

Quant Decision Full Suite Verification:
- Status: VERIFIED
- Last verified:
  - full test suite passed: 209 passed

Quant Decision Guard Phase Closed:
- Status: CLOSED
- Scope closed: quant formulas, enriched market payload fields, market snapshot canonicalization, adapter raw payload dropping, quant signal canonical fields, decision context quant signal guard, decision threshold boundary coverage.
- Out of scope remains: broker execution, IBKR, live orders, paid APIs, ML training loop.
- Last verified:
  - full test suite passed: 209 passed

Outcome Measurement Foundation Started:
- Status: IMPLEMENTED
- Contract: docs/contracts/outcome-measurement-contract-v1.md
- Model: src/app/models/outcome_record.py
- Tests: tests/test_outcome_record.py
- Implemented: OutcomeRecord, OUTCOME_RECORD_FIELDS, validate_outcome_record, calculate_return_pct, build_outcome_record.
- Scope remains analytics-only: no broker execution, no IBKR, no orders, no realized trade P&L.
- Last verified:
  - outcome tests passed: 10 passed
  - full test suite passed: 219 passed

Outcome Source Decision Link Guard Closed:
- Status: IMPLEMENTED
- Model guard: src/app/models/outcome_record.py validates source_decision_id as UUID.
- Contract: docs/contracts/outcome-measurement-contract-v1.md documents source_decision_id UUID rule.
- Last verified:
  - outcome tests passed: 11 passed
  - full test suite passed: 220 passed

Outcome Max Movement Calculations Closed:
- Status: IMPLEMENTED
- Helpers: calculate_max_up_pct and calculate_max_down_pct in src/app/models/outcome_record.py
- Contract: docs/contracts/outcome-measurement-contract-v1.md documents max_up_pct and max_down_pct formulas.
- Last verified:
  - outcome tests passed: 14 passed
  - full test suite passed: 223 passed
