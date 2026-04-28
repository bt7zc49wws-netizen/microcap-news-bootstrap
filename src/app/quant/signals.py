"""Build canonical quant signals from validated market snapshots.

This module must stay API-independent:
- no provider clients
- no network calls
- no database access
- no trading execution
"""

from __future__ import annotations

from app.quant.snapshot import validate_market_snapshot
from app.quant.formulas import (
    atr_pct,
    breakout_pct,
    close_location_value,
    dollar_volume,
    gap_pct,
    intraday_return_pct,
    price_change_pct,
    range_pct,
    relative_volume,
    vwap_distance_pct,
)


def build_quant_signal(
    *,
    current_price: float,
    open_price: float,
    high_price: float,
    low_price: float,
    previous_close: float,
    current_volume: float,
    average_volume: float,
    vwap_value: float,
    atr_value: float,
    breakout_level: float,
) -> dict[str, float]:
    """Build canonical quant signal output from validated market snapshot values."""
    return {
        "price_change_pct": price_change_pct(current_price, previous_close),
        "gap_pct": gap_pct(open_price, previous_close),
        "intraday_return_pct": intraday_return_pct(current_price, open_price),
        "relative_volume": relative_volume(current_volume, average_volume),
        "dollar_volume": dollar_volume(current_price, current_volume),
        "range_pct": range_pct(high_price, low_price, previous_close),
        "close_location_value": close_location_value(current_price, low_price, high_price),
        "vwap_distance_pct": vwap_distance_pct(current_price, vwap_value),
        "atr_pct": atr_pct(atr_value, current_price),
        "breakout_pct": breakout_pct(current_price, breakout_level),
    }

def build_quant_signal_from_snapshot(snapshot: dict[str, float]) -> dict[str, float]:
    """Validate a market snapshot and build canonical quant signal output."""
    validated = validate_market_snapshot(snapshot)
    return build_quant_signal(**validated)

