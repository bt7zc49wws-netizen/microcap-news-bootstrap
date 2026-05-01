from datetime import UTC, datetime

from app.services.execution.types import ExecutionLogEntry


def test_execution_log_entry_shape():
    now = datetime.now(UTC)

    entry = ExecutionLogEntry(
        execution_id="exec-1",
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=100,
        status="submitted",
        created_at=now,
        broker_name="ibkr",
    )

    assert entry.execution_id == "exec-1"
    assert entry.order_id == "order-1"
    assert entry.symbol == "ABCD"
    assert entry.side == "buy"
    assert entry.quantity == 100
    assert entry.status == "submitted"
    assert entry.created_at == now
    assert entry.broker_name == "ibkr"
    assert entry.fill_price is None
    assert entry.error_message is None
