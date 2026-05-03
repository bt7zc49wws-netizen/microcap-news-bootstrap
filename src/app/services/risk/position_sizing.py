from __future__ import annotations

from dataclasses import dataclass
from math import floor


@dataclass(frozen=True)
class PositionSizeResult:
    account_equity_usd: float
    risk_fraction: float
    risk_amount_usd: float
    entry_price: float
    stop_price: float
    risk_per_share: float
    quantity: int
    notional_usd: float


def calculate_position_size(
    *,
    account_equity_usd: float,
    risk_fraction: float,
    entry_price: float,
    stop_price: float,
) -> PositionSizeResult:
    if account_equity_usd <= 0:
        raise ValueError("account_equity_must_be_positive")
    if risk_fraction <= 0 or risk_fraction > 1:
        raise ValueError("risk_fraction_out_of_range")
    if entry_price <= 0 or stop_price <= 0:
        raise ValueError("prices_must_be_positive")
    if entry_price <= stop_price:
        raise ValueError("entry_price_must_exceed_stop_price")

    risk_amount_usd = account_equity_usd * risk_fraction
    risk_per_share = entry_price - stop_price
    quantity = floor(risk_amount_usd / risk_per_share)
    notional_usd = quantity * entry_price

    return PositionSizeResult(
        account_equity_usd=account_equity_usd,
        risk_fraction=risk_fraction,
        risk_amount_usd=risk_amount_usd,
        entry_price=entry_price,
        stop_price=stop_price,
        risk_per_share=risk_per_share,
        quantity=quantity,
        notional_usd=notional_usd,
    )
