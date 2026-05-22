from __future__ import annotations

def simulate_trade(entry_price: float, exit_price: float, size: float = 1.0) -> float:
    slippage = entry_price * 0.001
    return (exit_price - entry_price - slippage * 2) * size
