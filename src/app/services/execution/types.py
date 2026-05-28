from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class ExecutionLogEntry:
    execution_id: str
    order_id: str
    symbol: str
    side: str
    quantity: int
    status: str
    created_at: datetime
    broker_name: Optional[str] = None
    fill_price: Optional[float] = None
    execution_mode: Optional[str] = None
    error_message: Optional[str] = None
