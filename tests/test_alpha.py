from app.replay.alpha_replay import run_alpha_replay


def test_alpha_runs():
    events = [
        {
            "symbol": "AAPL",
            "quant_signal": {"price_change_pct": 5},
        },
        {
            "symbol": "TSLA",
            "quant_signal": {"price_change_pct": -3},
        },
        {
            "symbol": "NVDA",
            "quant_signal": {"price_change_pct": 8},
        },
    ]

    result = run_alpha_replay(events)

    assert "alpha_metrics" in result
    assert "alpha" in result["alpha_metrics"]
