"""Pure quantitative formula layer.

This package must stay API-independent:
- no provider clients
- no network calls
- no database access
- no trading execution
"""

from app.quant.signals import build_quant_signal
from app.quant.snapshot import REQUIRED_MARKET_SNAPSHOT_FIELDS, validate_market_snapshot
from app.quant.formulas import (
    price_change_pct,
    gap_pct,
    intraday_return_pct,
    relative_volume,
    dollar_volume,
    range_pct,
    close_location_value,
    vwap,
    vwap_distance_pct,
    true_range,
    atr,
    atr_pct,
    breakout_pct,
    slope,
    acceleration,
)

__all__ = [
    "build_quant_signal",
    "REQUIRED_MARKET_SNAPSHOT_FIELDS",
    "validate_market_snapshot",
    "price_change_pct",
    "gap_pct",
    "intraday_return_pct",
    "relative_volume",
    "dollar_volume",
    "range_pct",
    "close_location_value",
    "vwap",
    "vwap_distance_pct",
    "true_range",
    "atr",
    "atr_pct",
    "breakout_pct",
    "slope",
    "acceleration",
]
