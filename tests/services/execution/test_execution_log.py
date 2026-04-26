from app.services.execution.log import build_execution_log_entry


def test_build_execution_log_entry():
    entry = build_execution_log_entry(
        execution_id="exec-1",
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=100,
        status="submitted",
        broker_name="paper",
    )

    assert entry.execution_id == "exec-1"
    assert entry.order_id == "order-1"
    assert entry.symbol == "ABCD"
    assert entry.side == "buy"
    assert entry.quantity == 100
    assert entry.status == "submitted"
    assert entry.broker_name == "paper"
    assert entry.error_message is None
