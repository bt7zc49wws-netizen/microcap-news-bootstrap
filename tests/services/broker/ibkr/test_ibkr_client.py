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
