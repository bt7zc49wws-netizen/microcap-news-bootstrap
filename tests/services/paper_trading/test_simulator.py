from datetime import UTC, datetime

import pytest

from app.services.paper_trading.simulator import build_execution_log_entry, simulate_market_fill
from app.services.paper_trading.types import PaperOrder


def make_order(quantity: int = 100) -> PaperOrder:
    return PaperOrder(
        order_id="order-1",
        symbol="ABCD",
        side="buy",
        quantity=quantity,
        submitted_at=datetime.now(UTC),
    )


def test_simulate_market_fill():
    fill = simulate_market_fill(make_order(), fill_price=1.23)

    assert fill.order_id == "order-1"
    assert fill.symbol == "ABCD"
    assert fill.side == "buy"
    assert fill.quantity == 100
    assert fill.fill_price == 1.23


def test_simulate_market_fill_rejects_invalid_quantity():
    with pytest.raises(ValueError, match="order quantity must be greater than zero."):
        simulate_market_fill(make_order(quantity=0), fill_price=1.23)


def test_simulate_market_fill_rejects_invalid_price():
    with pytest.raises(ValueError, match="fill_price must be greater than zero."):
        simulate_market_fill(make_order(), fill_price=0)


def test_build_execution_log_entry():
    entry = build_execution_log_entry(make_order(), fill_price=1.23)

    assert entry.execution_id == "exec-order-1"
    assert entry.order_id == "order-1"
    assert entry.symbol == "ABCD"
    assert entry.side == "buy"
    assert entry.quantity == 100
    assert entry.status == "filled"
    assert entry.broker_name == "paper"
    assert entry.fill_price == 1.23


def test_paper_fill_and_execution_log_share_order_identity() -> None:
    order = make_order(quantity=250)
    fill = simulate_market_fill(order, fill_price=1.23)
    entry = build_execution_log_entry(order, fill_price=fill.fill_price)

    assert fill.order_id == entry.order_id
    assert fill.symbol == entry.symbol
    assert fill.side == entry.side
    assert fill.quantity == entry.quantity
    assert entry.broker_name == "paper"
    assert entry.fill_price == 1.23
