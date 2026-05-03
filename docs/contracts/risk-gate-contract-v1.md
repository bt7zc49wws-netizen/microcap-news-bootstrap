# Risk Gate Contract v1

Status: DRAFT

Purpose:
Define the pre-execution risk gate contract for validating paper/live-intent order candidates before any broker execution layer exists.

Scope:
- Safety/pre-execution validation only
- Applies before paper or future broker execution handoff
- No broker integration
- No IBKR
- No live orders
- No real capital movement

Inputs:
- order_value_usd
- realized_daily_loss_usd
- trades_today
- limits.max_position_usd
- limits.max_daily_loss_usd
- limits.max_trades_per_day

RiskCheckResult fields:
- allowed
- reason_code
- reason_label

Canonical reason codes:
- INVALID_ORDER_VALUE
- INVALID_DAILY_LOSS
- INVALID_TRADES_TODAY
- INVALID_RISK_LIMITS
- MAX_POSITION_EXCEEDED
- MAX_DAILY_LOSS_REACHED
- MAX_TRADES_REACHED
- RISK_CHECK_PASSED

Rules:
- order_value_usd must be positive.
- realized_daily_loss_usd must not be negative.
- trades_today must not be negative.
- all risk limits must be positive.
- order_value_usd greater than max_position_usd must be rejected.
- realized_daily_loss_usd greater than or equal to max_daily_loss_usd must be rejected.
- trades_today greater than or equal to max_trades_per_day must be rejected.
- allowed results must use reason_code RISK_CHECK_PASSED and reason_label Risk check passed.
- reason_code must remain inside the canonical reason code set.

Out of scope:
- position sizing
- broker submission
- IBKR
- live order placement
- realized trade P&L
