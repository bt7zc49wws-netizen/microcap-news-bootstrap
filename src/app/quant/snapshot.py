"""Validate provider-independent market snapshot inputs for quant signal building."""

from __future__ import annotations

REQUIRED_MARKET_SNAPSHOT_FIELDS = (
    "current_price",
    "open_price",
    "high_price",
    "low_price",
    "previous_close",
    "current_volume",
    "average_volume",
    "vwap_value",
    "atr_value",
    "breakout_level",
)


def validate_market_snapshot(snapshot: dict[str, float]) -> dict[str, float]:
    """Validate and return a provider-independent market snapshot."""
    missing_fields = [
        field for field in REQUIRED_MARKET_SNAPSHOT_FIELDS if field not in snapshot
    ]
    if missing_fields:
        raise ValueError(f"missing required market snapshot fields: {missing_fields}")

    validated: dict[str, float] = {}
    for field in REQUIRED_MARKET_SNAPSHOT_FIELDS:
        value = snapshot[field]
        if not isinstance(value, int | float):
            raise ValueError(f"{field} must be numeric")
        validated[field] = float(value)

    return validated
