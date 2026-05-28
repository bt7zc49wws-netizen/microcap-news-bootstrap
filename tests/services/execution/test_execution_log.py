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
        fill_price=1.23,
    )

    assert entry.execution_id == "exec-1"
    assert entry.order_id == "order-1"
    assert entry.symbol == "ABCD"
    assert entry.side == "buy"
    assert entry.quantity == 100
    assert entry.status == "submitted"
    assert entry.broker_name == "paper"
    assert entry.fill_price == 1.23
    assert entry.execution_mode is None
    assert entry.error_message is None


def test_build_execution_log():
    from datetime import datetime, timezone
    from app.services.execution.log import build_execution_log
    from app.services.paper_trading.types import PaperFill

    fill = PaperFill(
        order_id=\"paper-aapl-1\",
        symbol=\"AAPL\",
        side=\"BUY\",
        quantity=5,
        fill_price=189.25,
        filled_at=datetime.now(timezone.utc),
    )

    log = build_execution_log(fill=fill, pnl=46.25)

    assert log.symbol == \"AAPL\"
    assert log.pnl == 46.25
