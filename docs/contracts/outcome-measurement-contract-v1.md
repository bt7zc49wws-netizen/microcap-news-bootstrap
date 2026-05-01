# Outcome Measurement Contract v1

Status: DRAFT

Purpose:
Define the offline-safe outcome record shape used to measure decision results after the fact.

Scope:
- Post-decision measurement only
- No broker integration
- No trading execution
- No order generation
- No live paid API dependency
- No ML training loop in this phase

Canonical outcome record fields:
- source_decision_id
- symbol
- decision
- measured_at_utc
- horizon_minutes
- reference_price
- observed_price
- return_pct
- max_up_pct
- max_down_pct

Rules:
- source_decision_id links back to the decision snapshot/result being measured.
- symbol must be uppercase.
- decision must remain one of no_trade, watchlist, actionable.
- measured_at_utc must be UTC ISO-8601 text.
- horizon_minutes must be a positive integer.
- reference_price and observed_price must be positive numbers.
- return_pct is measured from reference_price to observed_price using ((observed_price - reference_price) / reference_price) * 100.0.
- build_outcome_record must calculate return_pct from reference_price and observed_price, then validate the canonical record shape.
- max_up_pct and max_down_pct are optional adverse/favorable movement metrics for the same horizon.
- Outcome records are analytics-only and must not trigger execution.

Out of scope:
- IBKR
- broker accounts
- position sizing
- order placement
- realized P&L from actual trades
- online learning
