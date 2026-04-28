"""Derive provider-independent market snapshot inputs from normalized OHLCV series.

Rules:
- no paid API dependency
- no trading execution
- no broker integration
- no provider client calls
- pure transformation only
"""

from __future__ import annotations

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

