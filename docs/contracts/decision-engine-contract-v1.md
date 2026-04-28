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
