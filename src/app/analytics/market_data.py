"""Minimal market outcome layer (replace with IB data later)."""

from __future__ import annotations


def get_price_series(symbol: str) -> list[float]:
    # placeholder deterministic series
    base = abs(hash(symbol)) % 100 + 50
    return [base + i * 0.5 for i in range(10)]


def compute_return(symbol: str, horizon: int = 5) -> float:
    series = get_price_series(symbol)
    if len(series) < horizon + 1:
        return 0.0

    return (series[horizon] - series[0]) / series[0]
