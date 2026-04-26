from datetime import UTC, datetime

from app.services.paper_trading.types import PaperFill, PaperOrder


def test_paper_order_shape():
    now = datetime.now(UTC)

    order = PaperOrder(
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=100,
        submitted_at=now,
    )

    assert order.order_id == "order-1"
    assert order.symbol == "ABCD"
    assert order.side == "buy"
    assert order.quantity == 100
    assert order.status == "submitted"


def test_paper_fill_shape():
    now = datetime.now(UTC)

    fill = PaperFill(
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=100,
        fill_price=1.23,
        filled_at=now,
    )

    assert fill.order_id == "order-1"
    assert fill.symbol == "ABCD"
    assert fill.fill_price == 1.23
