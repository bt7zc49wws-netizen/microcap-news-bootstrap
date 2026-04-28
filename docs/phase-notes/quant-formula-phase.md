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
