from __future__ import annotations

class PortfolioState:
    def __init__(self, capital: float = 10000.0):
        self.capital = capital
        self.positions = {}
        self.pnl = 0.0

    def exposure(self) -> float:
        return sum(self.positions.values())

    def available_capital(self) -> float:
        return self.capital - self.exposure()
