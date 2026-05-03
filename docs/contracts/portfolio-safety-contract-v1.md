# Portfolio Safety Contract v1

Status: Accepted Draft

Purpose:
Define analytics-only portfolio and buying-power safety checks before any broker execution layer exists.

Scope:
- Portfolio exposure and buying-power validation only
- Pre-execution safety support
- No broker integration
- No IBKR
- No live orders
- No real capital movement

Inputs:
- account_equity_usd
- available_cash_usd
- current_exposure_usd
- proposed_notional_usd
- max_total_exposure_fraction
- min_cash_buffer_fraction

Output fields:
- allowed
- reason_code
- reason_label
- projected_exposure_usd
- projected_exposure_fraction
- projected_cash_usd
- projected_cash_buffer_fraction

Canonical reason codes:
- INVALID_PORTFOLIO_INPUTS
- MAX_EXPOSURE_EXCEEDED
- CASH_BUFFER_BREACHED
- PORTFOLIO_CHECK_PASSED

Rules:
- account_equity_usd must be positive.
- available_cash_usd must not be negative.
- current_exposure_usd must not be negative.
- proposed_notional_usd must be positive.
- max_total_exposure_fraction must be greater than 0 and less than or equal to 1.
- min_cash_buffer_fraction must be greater than or equal to 0 and less than 1.
- projected_exposure_usd = current_exposure_usd + proposed_notional_usd.
- projected_exposure_fraction = projected_exposure_usd / account_equity_usd.
- projected_cash_usd = available_cash_usd - proposed_notional_usd.
- projected_cash_buffer_fraction = projected_cash_usd / account_equity_usd.
- projected_exposure_fraction greater than max_total_exposure_fraction must be rejected.
- projected_cash_buffer_fraction less than min_cash_buffer_fraction must be rejected.

Out of scope:
- broker buying power API reads
- margin rules
- portfolio optimization
- order submission
- IBKR
- live orders
