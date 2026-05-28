import pytest

from app.services.broker.ibkr.client import IbkrPaperClient


def test_ibkr_paper_client_disabled_by_default():
    client = IbkrPaperClient()

    with pytest.raises(RuntimeError, match="IBKR paper trading is disabled."):
        client.submit_paper_order(
            order_id="order-1",
            symbol="ABCD",
            side="buy",
            quantity=100,
        )


def test_ibkr_paper_client_submits_order_when_enabled():
    client = IbkrPaperClient(enabled=True)

    order = client.submit_paper_order(
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=100,
    )

    assert order.order_id == "order-1"
    assert order.symbol == "ABCD"
    assert order.side == "buy"
    assert order.quantity == 100
    assert order.status == "submitted"
    assert order.execution_mode == "paper"


def test_confirm_fill_returns_fill_object():
    from app.services.broker.ibkr.client import IbkrPaperClient

    client = IbkrPaperClient(enabled=True)

    order = client.submit_paper_order(
        order_id=\"paper-aapl-1\",
        symbol=\"AAPL\",
        side=\"BUY\",
        quantity=5,
    )

    fill = client.confirm_fill(order=order, fill_price=189.25)

    assert fill.symbol == \"AAPL\"
    assert fill.side == \"BUY\"
    assert fill.quantity == 5
    assert fill.fill_price == 189.25


def test_open_orders_tracking():
    from app.services.broker.ibkr.client import IbkrPaperClient

    client = IbkrPaperClient(enabled=True)

    order = client.submit_paper_order(
        order_id=\"paper-aapl-open-1\",
        symbol=\"AAPL\",
        side=\"BUY\",
        quantity=1,
    )

    open_orders = client.get_open_orders()

    assert len(open_orders) >= 1
    assert any(o.order_id == order.order_id for o in open_orders)


def test_open_orders_persist_after_multiple_submissions():
    from app.services.broker.ibkr.client import IbkrPaperClient

    client = IbkrPaperClient(enabled=True)

    client.submit_paper_order(order_id=\"paper-aapl-1\", symbol=\"AAPL\", side=\"BUY\", quantity=1)
    client.submit_paper_order(order_id=\"paper-aapl-2\", symbol=\"AAPL\", side=\"BUY\", quantity=2)

    open_orders = client.get_open_orders()

    assert len(open_orders) == 2
