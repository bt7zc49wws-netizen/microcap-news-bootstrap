from __future__ import annotations

def compute_future_return(event: dict) -> float:
    q = event.get("quant_signal", {})
    price_change = q.get("price_change_pct", 0.0)
    return price_change * 0.5
