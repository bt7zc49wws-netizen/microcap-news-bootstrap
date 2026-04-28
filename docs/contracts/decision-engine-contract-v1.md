# Decision Engine Contract v1

Status: DRAFT

Purpose:
Define the offline-safe canonical decision result shape.

Scope:
- Decision result construction only
- No scoring
- No live provider calls
- No paid API dependency
- No broker integration
- No trading execution
- No order generation

Canonical decisions:
- no_trade
- watchlist
- actionable

Builder:
- Function: make_decision_result
- Module: src/app/decision_engine.py
- Smoke: scripts/quant/smoke_decision_engine.py

Output fields:
- decision
- reason_codes

Rules:
- decision must be one of the canonical decisions
- reason_codes must not be empty
- legacy decision names such as trade/watch/pass must not be used
- engine must remain offline-safe


Evaluator:
- Function: evaluate_decision_context
- Module: src/app/decision_engine.py
- Smoke: scripts/quant/smoke_decision_engine.py

Initial deterministic rules:
- news event present + price_change_pct >= 10.0 + relative_volume >= 2.0 => actionable
- news event present without strong quant confirmation => watchlist
- no qualifying news event => no_trade

Evaluator rules:
- Evaluator must remain offline-safe.
- Evaluator must not perform scoring.
- Evaluator must not call providers.
- Evaluator must not perform trading execution.
- Evaluator must return canonical decision result shape.


Supported news event gate:
- Constant: SUPPORTED_NEWS_EVENT_TYPES
- Module: src/app/decision_engine.py

Supported initial event types:
- financing
- dilution
- offering
- clinical
- fda
- earnings
- merger
- contract

Gate rules:
- Unsupported or missing news event type => no_trade
- Supported news event + price_change_pct >= 10.0 + relative_volume >= 2.0 => actionable
- Supported news event without strong quant confirmation => watchlist

Reason codes:
- SUPPORTED_NEWS_EVENT
- UNSUPPORTED_OR_MISSING_NEWS_EVENT
- PRICE_CHANGE_STRONG
- RELATIVE_VOLUME_STRONG


Default thresholds:
- Constant: DEFAULT_DECISION_THRESHOLDS
- Module: src/app/decision_engine.py

Initial threshold values:
- strong_price_change_pct: 10.0
- strong_relative_volume: 2.0

Threshold rules:
- Evaluator must read strong quant confirmation from DEFAULT_DECISION_THRESHOLDS.
- Threshold changes require tests.
- Thresholds are static defaults for now.
- No live config service is introduced in this phase.


Reason code registry:
- Constants:
  - REASON_SUPPORTED_NEWS_EVENT
  - REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT
  - REASON_PRICE_CHANGE_STRONG
  - REASON_RELATIVE_VOLUME_STRONG
- Registry: VALID_REASON_CODES
- Module: src/app/decision_engine.py

Registry rules:
- Evaluator must use reason code constants.
- New reason codes must be added to VALID_REASON_CODES.
- Reason code changes require tests.
- Reason codes are API/dashboard/replay-facing identifiers.


Decision result trace:
- Optional field: symbol
- Source: decision context symbol
- Normalization: uppercase
- Applies to evaluate_decision_context outputs

Trace rules:
- make_decision_result may include symbol when provided.
- Empty symbol must be rejected when symbol is explicitly provided.
- Evaluator should preserve symbol trace from decision context.
- Symbol trace is for API/dashboard/replay observability only.
