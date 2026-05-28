from typing import Optional
from datetime import datetime, timezone

from app.services.execution.types import ExecutionLogEntry


def build_execution_log_entry(
    *,
    execution_id: str,
    order_id: str,
    symbol: str,
    side: str,
    quantity: int,
    status: str,
    broker_name: Optional[str] = None,
    fill_price: Optional[float] = None,
    execution_mode: Optional[str] = None,
    error_message: Optional[str] = None,
) -> ExecutionLogEntry:
    return ExecutionLogEntry(
        execution_id=execution_id,
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        status=status,
        created_at=datetime.now(timezone.utc),
        broker_name=broker_name,
        fill_price=fill_price,
        execution_mode=execution_mode,
        error_message=error_message,
    )

from dataclasses import dataclass
from typing import Optional
from app.services.paper_trading.types import PaperFill

@dataclass(frozen=True)
class ExecutionLog:
    symbol: str
    side: str
    quantity: int
    fill_price: float
    pnl: float


def build_execution_log(fill: PaperFill, pnl: float) -> ExecutionLog:
    return ExecutionLog(
        symbol=fill.symbol,
        side=fill.side,
        quantity=fill.quantity,
        fill_price=fill.fill_price,
        pnl=pnl,
    )
