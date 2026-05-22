from __future__ import annotations

from app.analytics.market_data import compute_return


def label_event(event: dict) -> float:
    symbol = event["input"]["symbol"]
    return compute_return(symbol)
