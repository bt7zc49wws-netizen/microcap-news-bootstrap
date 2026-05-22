from app.live.engine import run_live
from app.portfolio.state import PortfolioState


def test_live_engine():
    state = PortfolioState()

    event = {
        "symbol": "AAPL",
        "quant_signal": {"price_change_pct": 5.0},
        "news": {"event_type": "generic_pr"}
    }

    result = run_live(event, state)

    assert "status" in result
