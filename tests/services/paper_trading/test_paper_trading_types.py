from datetime import datetime, timezone

from app.services.paper_trading.types import PaperFill, PaperOrder


def test_paper_order_shape():
    now = datetime.now(timezone.utc)

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
    assert order.execution_mode == "paper"


def test_paper_fill_shape():
    now = datetime.now(timezone.utc)

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
    assert fill.execution_mode == "paper"


def test_position_state_pnl_calculation():
    from app.services.paper_trading.types import PositionState

    position = PositionState(
        symbol=\"AAPL\",
        quantity=5,
        average_price=180.0,
        market_price=189.25,
    )

    assert position.pnl == 46.25


def test_run_aapl_paper_trade():
    from app.services.paper_trading.run_aapl_trade import run_aapl_paper_trade

    result = run_aapl_paper_trade()

    assert result[\"status\"] == \"PAPER TRADE EXECUTED\"
    assert result[\"symbol\"] == \"AAPL\"
    assert result[\"side\"] == \"BUY\"
    assert result[\"position_open\"] is True


def test_position_state_positive_pnl_snapshot():
    from app.services.paper_trading.types import PositionState

    position = PositionState(
        symbol=\"AAPL\",
        quantity=5,
        average_price=189.25,
        market_price=194.25,
    )

    assert position.pnl == 25.0
