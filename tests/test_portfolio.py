from app.portfolio.state import PortfolioState
from app.live.run_loop import run_once


def test_portfolio_flow():
    state = PortfolioState(capital=10000)

    event = {
        "symbol": "AAPL",
        "quant_signal": {"price_change_pct": 10.0},
        "news": {"event_type": "generic_pr"},
    }

    result = run_once(state, event)

    assert "status" in result
