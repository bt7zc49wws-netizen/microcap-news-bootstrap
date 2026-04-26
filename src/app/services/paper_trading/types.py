from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class PaperOrder:
    order_id: str
    symbol: str
    side: str
    quantity: int
    submitted_at: datetime
    status: str = "submitted"


@dataclass(frozen=True, slots=True)
class PaperFill:
    order_id: str
    symbol: str
    side: str
    quantity: int
    fill_price: float
    filled_at: datetime
