from datetime import UTC, datetime

from app.services.execution.types import ExecutionLogEntry
from app.services.paper_trading.types import PaperFill, PaperOrder


def simulate_market_fill(order: PaperOrder, fill_price: float) -> PaperFill:
    if order.quantity <= 0:
        raise ValueError("order quantity must be greater than zero.")
    if fill_price <= 0:
        raise ValueError("fill_price must be greater than zero.")

    return PaperFill(
        order_id=order.order_id,
        symbol=order.symbol,
        side=order.side,
        quantity=order.quantity,
        fill_price=fill_price,
        filled_at=datetime.now(UTC),
    )


def build_execution_log_entry(
    order: PaperOrder,
    status: str = "filled",
    fill_price: float | None = None,
) -> ExecutionLogEntry:
    return ExecutionLogEntry(
        execution_id=f"exec-{order.order_id}",
        order_id=order.order_id,
        symbol=order.symbol,
        side=order.side,
        quantity=order.quantity,
        status=status,
        created_at=datetime.now(UTC),
        broker_name="paper",
        fill_price=fill_price,
    )
