from datetime import UTC, datetime

from app.services.execution.types import ExecutionLogEntry


def build_execution_log_entry(
    *,
    execution_id: str,
    order_id: str,
    symbol: str,
    side: str,
    quantity: int,
    status: str,
    broker_name: str | None = None,
    fill_price: float | None = None,
    execution_mode: str | None = None,
    error_message: str | None = None,
) -> ExecutionLogEntry:
    return ExecutionLogEntry(
        execution_id=execution_id,
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        status=status,
        created_at=datetime.now(UTC),
        broker_name=broker_name,
        fill_price=fill_price,
        execution_mode=execution_mode,
        error_message=error_message,
    )
