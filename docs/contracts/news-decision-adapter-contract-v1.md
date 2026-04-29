# News Decision Adapter Contract v1

Status: DRAFT

Purpose:
Define how news classification output is adapted into decision-context news input.

Scope:
- Offline-safe adaptation only
- No live provider calls
- No paid API dependency
- No broker integration
- No trading execution
- No scoring

Adapter:
- Function: adapt_news_for_decision
- Module: src/app/news_decision_adapter.py
- Smoke: scripts/quant/smoke_news_decision_adapter.py

Required classification inputs:
- event_type
- headline

Decision-context news output:
- event_type
- headline

Rules:
- event_type must not be empty
- headline must not be empty
- provider/classifier extra fields must not leak into decision-context news input
- adapter must remain pure validation/adaptation


End-to-end decision path:
- Smoke: scripts/quant/smoke_news_to_decision.py

Offline E2E chain:
- classification output
- adapt_news_for_decision
- build_decision_context
- evaluate_decision_context
- canonical decision result

E2E rules:
- The chain must remain offline-safe.
- The chain must not call live providers.
- The chain must not use paid APIs.
- The chain must not perform broker, order, or execution operations.


Full Offline Decision Pipeline Smoke:
- Smoke: scripts/quant/smoke_full_offline_decision_pipeline.py
- Chain:
  - Stooq OHLCV rows
  - normalize_stooq_ohlcv_rows
  - enrich_stooq_market_payload
  - adapt_stooq_market_snapshot
  - build_quant_signal_from_snapshot
  - classification output
  - adapt_news_for_decision
  - build_decision_context
  - evaluate_decision_context
  - canonical decision result

Full offline pipeline rules:
- The smoke must remain offline-safe.
- The smoke must not call live providers.
- The smoke must not use paid APIs.
- The smoke must not perform broker, IBKR, order, or execution operations.
- The smoke validates integration shape only; it is not a trading recommendation or execution path.


Decision Context Audit Trace:
- `build_decision_context` may include optional `audit_trace`.
- `audit_trace` is for offline-safe traceability only.
- `audit_trace` must be omitted or non-empty.
- Empty `audit_trace` is invalid.
- `audit_trace` must not introduce live provider calls, paid API dependency, broker integration, IBKR dependency, order generation, or trading execution.
- Current smoke usage may identify the offline pipeline/source path, for example:
  - market_source
  - news_source
  - pipeline


Offline Decision Result Fixture:
- Fixture: tests/fixtures/offline_decision/full_offline_decision_result.json
- The full offline decision smoke must validate the canonical decision result against this committed fixture.
- Fixture changes require smoke + full test before commit.
- Fixture validation remains offline-safe and must not introduce live providers, paid APIs, broker, IBKR, order generation, or trading execution.


Decision Result Audit Boundary:
- `audit_trace` belongs to decision context, not canonical decision result.
- `evaluate_decision_context` must not copy `audit_trace` into the decision result.
- Canonical decision result remains limited to decision, reason_codes, and optional symbol.
- Full offline fixture intentionally excludes audit_trace.
