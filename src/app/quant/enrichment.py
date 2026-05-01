"""Derive provider-independent market snapshot inputs from normalized OHLCV series.

Rules:
- no paid API dependency
- no trading execution
- no broker integration
- no provider client calls
- pure transformation only
"""

from __future__ import annotations

ENRICHED_MARKET_PAYLOAD_FIELDS = (
    "close",
    "open",
    "high",
    "low",
    "volume",
    "previous_close",
    "average_volume",
    "vwap",
    "atr",
    "breakout_level",
)


def derive_previous_close(ohlcv_rows: list[dict[str, float]]) -> float:
    """Return previous close from the second-to-last OHLCV row."""
    if len(ohlcv_rows) < 2:
        raise ValueError("ohlcv_rows must contain at least two rows")

    previous_close = ohlcv_rows[-2]["close"]
    if not isinstance(previous_close, int | float):
        raise ValueError("previous close must be numeric")

    return float(previous_close)


def derive_average_volume(ohlcv_rows: list[dict[str, float]], lookback: int = 20) -> float:
    """Return average volume over the latest completed rows before the current row."""
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if len(ohlcv_rows) < 2:
        raise ValueError("ohlcv_rows must contain at least two rows")

    completed_rows = ohlcv_rows[:-1]
    selected_rows = completed_rows[-lookback:]

    volumes: list[float] = []
    for row in selected_rows:
        volume = row["volume"]
        if not isinstance(volume, int | float):
            raise ValueError("volume must be numeric")
        volumes.append(float(volume))

    if not volumes:
        raise ValueError("no completed volume rows available")

    return sum(volumes) / len(volumes)


def derive_vwap(ohlcv_rows: list[dict[str, float]], lookback: int = 20) -> float:
    """Return VWAP over latest completed rows before the current row.

    Uses typical price per row:
    (high + low + close) / 3
    """
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if len(ohlcv_rows) < 2:
        raise ValueError("ohlcv_rows must contain at least two rows")

    completed_rows = ohlcv_rows[:-1]
    selected_rows = completed_rows[-lookback:]

    total_price_volume = 0.0
    total_volume = 0.0

    for row in selected_rows:
        high = row["high"]
        low = row["low"]
        close = row["close"]
        volume = row["volume"]

        if not isinstance(high, int | float):
            raise ValueError("high must be numeric")
        if not isinstance(low, int | float):
            raise ValueError("low must be numeric")
        if not isinstance(close, int | float):
            raise ValueError("close must be numeric")
        if not isinstance(volume, int | float):
            raise ValueError("volume must be numeric")

        typical_price = (float(high) + float(low) + float(close)) / 3.0
        total_price_volume += typical_price * float(volume)
        total_volume += float(volume)

    if total_volume <= 0:
        raise ValueError("total volume must be positive")

    return total_price_volume / total_volume


def derive_atr(ohlcv_rows: list[dict[str, float]], lookback: int = 14) -> float:
    """Return average true range over latest completed rows before the current row."""
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if len(ohlcv_rows) < 3:
        raise ValueError("ohlcv_rows must contain at least three rows")

    completed_rows = ohlcv_rows[:-1]
    selected_rows = completed_rows[-lookback:]

    if len(selected_rows) < 2:
        raise ValueError("at least two completed rows are required")

    true_ranges: list[float] = []

    for index in range(1, len(selected_rows)):
        row = selected_rows[index]
        previous_row = selected_rows[index - 1]

        high = row["high"]
        low = row["low"]
        previous_close = previous_row["close"]

        if not isinstance(high, int | float):
            raise ValueError("high must be numeric")
        if not isinstance(low, int | float):
            raise ValueError("low must be numeric")
        if not isinstance(previous_close, int | float):
            raise ValueError("previous close must be numeric")

        true_ranges.append(
            max(
                float(high) - float(low),
                abs(float(high) - float(previous_close)),
                abs(float(low) - float(previous_close)),
            )
        )

    return sum(true_ranges) / len(true_ranges)


def derive_breakout_level(ohlcv_rows: list[dict[str, float]], lookback: int = 20) -> float:
    """Return breakout level as highest high over latest completed rows before current row."""
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if len(ohlcv_rows) < 2:
        raise ValueError("ohlcv_rows must contain at least two rows")

    completed_rows = ohlcv_rows[:-1]
    selected_rows = completed_rows[-lookback:]

    highs: list[float] = []
    for row in selected_rows:
        high = row["high"]
        if not isinstance(high, int | float):
            raise ValueError("high must be numeric")
        highs.append(float(high))

    if not highs:
        raise ValueError("no completed high rows available")

    return max(highs)


def enrich_stooq_market_payload(
    ohlcv_rows: list[dict[str, float]],
    *,
    average_volume_lookback: int = 20,
    vwap_lookback: int = 20,
    atr_lookback: int = 14,
    breakout_lookback: int = 20,
) -> dict[str, float]:
    """Build normalized Stooq-like payload with derived snapshot fields."""
    if not ohlcv_rows:
        raise ValueError("ohlcv_rows must not be empty")

    current_row = ohlcv_rows[-1]

    return {
        "close": float(current_row["close"]),
        "open": float(current_row["open"]),
        "high": float(current_row["high"]),
        "low": float(current_row["low"]),
        "volume": float(current_row["volume"]),
        "previous_close": derive_previous_close(ohlcv_rows),
        "average_volume": derive_average_volume(ohlcv_rows, lookback=average_volume_lookback),
        "vwap": derive_vwap(ohlcv_rows, lookback=vwap_lookback),
        "atr": derive_atr(ohlcv_rows, lookback=atr_lookback),
        "breakout_level": derive_breakout_level(ohlcv_rows, lookback=breakout_lookback),
    }

