# Position Sizing Contract v1

Status: DRAFT

Purpose:
Define analytics-only position sizing calculations before any broker execution layer exists.

Scope:
- Position sizing calculation only
- Pre-execution safety support
- No broker integration
- No IBKR
- No live orders
- No real capital movement

Inputs:
- account_equity_usd
- risk_fraction
- entry_price
- stop_price

Output fields:
- account_equity_usd
- risk_fraction
- risk_amount_usd
- entry_price
- stop_price
- risk_per_share
- quantity
- notional_usd

Rules:
- account_equity_usd must be positive.
- risk_fraction must be greater than 0 and less than or equal to 1.
- entry_price must be positive.
- stop_price must be positive.
- entry_price must be greater than stop_price for long-side sizing.
- risk_amount_usd = account_equity_usd * risk_fraction.
- risk_per_share = entry_price - stop_price.
- quantity = floor(risk_amount_usd / risk_per_share).
- notional_usd = quantity * entry_price.
- quantity must be non-negative.

Out of scope:
- short-side sizing
- portfolio allocation
- buying power checks
- broker submission
- IBKR
- live orders
