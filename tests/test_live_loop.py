from app.live.run_loop import run_once


def test_run_once_does_not_crash():
    event = {
        "symbol": "AAPL",
        "quant_signal": {"price_change_pct": 5.0},
        "news": {"event_type": "generic_pr"},
    }

    result = run_once(event)

    assert "status" in result
