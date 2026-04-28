"""API-independent market signal formulas."""

from __future__ import annotations


def _require_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def price_change_pct(current_price: float, previous_close: float) -> float:
    """Return percent change from previous close to current price."""
    _require_positive(previous_close, "previous_close")
    return ((current_price - previous_close) / previous_close) * 100.0


def gap_pct(open_price: float, previous_close: float) -> float:
    """Return opening gap percent versus previous close."""
    _require_positive(previous_close, "previous_close")
    return ((open_price - previous_close) / previous_close) * 100.0


def intraday_return_pct(current_price: float, open_price: float) -> float:
    """Return intraday percent return from open to current price."""
    _require_positive(open_price, "open_price")
    return ((current_price - open_price) / open_price) * 100.0


def relative_volume(current_volume: float, average_volume: float) -> float:
    """Return current volume divided by average volume."""
    _require_positive(average_volume, "average_volume")
    return current_volume / average_volume


def dollar_volume(price: float, volume: float) -> float:
    """Return traded notional value."""
    return price * volume


def range_pct(high_price: float, low_price: float, reference_price: float) -> float:
    """Return high-low range as percent of reference price."""
    _require_positive(reference_price, "reference_price")
    return ((high_price - low_price) / reference_price) * 100.0


def close_location_value(close_price: float, low_price: float, high_price: float) -> float:
    """Return close location value in range [-1, 1].

    -1 means close at low.
     0 means close at midpoint.
     1 means close at high.
    """
    price_range = high_price - low_price
    _require_positive(price_range, "high_price - low_price")
    return ((close_price - low_price) / price_range) * 2.0 - 1.0

def vwap(total_price_volume: float, total_volume: float) -> float:
    """Return volume-weighted average price from aggregated price*volume and volume."""
    _require_positive(total_volume, "total_volume")
    return total_price_volume / total_volume


def vwap_distance_pct(price: float, vwap_value: float) -> float:
    """Return price distance from VWAP as percent."""
    _require_positive(vwap_value, "vwap_value")
    return ((price - vwap_value) / vwap_value) * 100.0

def true_range(high_price: float, low_price: float, previous_close: float) -> float:
    """Return true range for one period."""
    return max(
        high_price - low_price,
        abs(high_price - previous_close),
        abs(low_price - previous_close),
    )


def atr(true_ranges: list[float]) -> float:
    """Return simple average true range from a list of true range values."""
    if not true_ranges:
        raise ValueError("true_ranges must not be empty")
    return sum(true_ranges) / len(true_ranges)


def atr_pct(atr_value: float, reference_price: float) -> float:
    """Return ATR as percent of reference price."""
    _require_positive(reference_price, "reference_price")
    return (atr_value / reference_price) * 100.0

def breakout_pct(price: float, breakout_level: float) -> float:
    """Return price distance from breakout level as percent.

    Positive means price is above the breakout level.
    Negative means price is below the breakout level.
    """
    _require_positive(breakout_level, "breakout_level")
    return ((price - breakout_level) / breakout_level) * 100.0

