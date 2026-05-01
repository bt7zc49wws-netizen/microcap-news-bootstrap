from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ExecutionLogEntry:
    execution_id: str
    order_id: str
    symbol: str
    side: str
    quantity: int
    status: str
    created_at: datetime
    broker_name: str | None = None
    fill_price: float | None = None
    error_message: str | None = None
