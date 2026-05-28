from app.services.execution.log import build_execution_log
from app.services.paper_trading.types import PositionState
from app.services.risk.gate import kill_switch_active
from app.services.risk.types import RiskLimits


def run_aapl_paper_trade():
    from app.services.broker.ibkr.client import IbkrPaperClient
    from app.services.risk.gate import check_order_risk

    if kill_switch_active():
        raise RuntimeError("Kill switch active")

    limits = RiskLimits(
        max_position_usd=5000.0,
        max_daily_loss_usd=1000.0,
        max_trades_per_day=5,
    )

    risk = check_order_risk(
        order_value_usd=946.25,
        realized_daily_loss_usd=0.0,
        trades_today=0,
        limits=limits,
    )

    if not risk.allowed:
        raise RuntimeError(risk.reason_code)

    client = IbkrPaperClient(enabled=True)

    order = client.submit_paper_order(
        order_id="paper-aapl-1",
        symbol="AAPL",
        side="BUY",
        quantity=5,
    )

    fill = client.confirm_fill(order=order, fill_price=189.25)

    position = PositionState(
        symbol="AAPL",
        quantity=5,
        average_price=189.25,
        market_price=189.25,
    )

    log = build_execution_log(fill=fill, pnl=position.pnl)

    return {
        "status": "PAPER TRADE EXECUTED",
        "symbol": log.symbol,
        "side": log.side,
        "qty": log.quantity,
        "fill_price": log.fill_price,
        "position_open": position.quantity > 0,
        "pnl": log.pnl,
    }
