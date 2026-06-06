from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PaperOrder:
    order_id: str
    symbol: str
    side: str
    quantity: int
    submitted_at: datetime
    status: str = "submitted"
    execution_mode: str = "paper"


@dataclass(frozen=True)
class PaperFill:
    order_id: str
    symbol: str
    side: str
    quantity: int
    fill_price: float
    filled_at: datetime
    execution_mode: str = "paper"


@dataclass(frozen=True)
class PositionState:
    symbol: str
    quantity: int
    average_price: float
    market_price: float

    @property
    def pnl(self) -> float:
        return round((self.market_price - self.average_price) * self.quantity, 2)
