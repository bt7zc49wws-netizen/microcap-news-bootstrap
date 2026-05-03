# Performance Feedback Contract v1

Status: DRAFT

Purpose:
Define analytics-only feedback records that connect decision snapshots to measured outcomes before any ML training loop exists.

Scope:
- Post-decision performance feedback only
- Uses existing decision_id / outcome measurement linkage
- No model training
- No online learning
- No broker integration
- No IBKR
- No live orders
- No real capital movement

Canonical feedback fields:
- source_decision_id
- symbol
- decision
- horizon_minutes
- return_pct
- max_up_pct
- max_down_pct
- was_directionally_positive
- feedback_label

Rules:
- source_decision_id must be a UUID string.
- symbol must be uppercase.
- decision must remain one of no_trade, watchlist, actionable.
- horizon_minutes must be positive.
- return_pct, max_up_pct, and max_down_pct are copied from the validated outcome record.
- was_directionally_positive is true when return_pct is greater than 0.
- feedback_label must be one of positive, neutral, negative.
- Feedback records are analytics-only and must not trigger execution or training automatically.

Out of scope:
- ML training loop
- model weight updates
- automated threshold tuning
- broker execution
- IBKR
- live orders
