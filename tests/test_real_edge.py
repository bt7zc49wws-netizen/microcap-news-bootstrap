from app.replay.analytics_replay import run_replay_with_metrics


def test_real_edge_runs() -> None:
    events = [
        {
            "symbol": "AAPL",
            "quant_signal": {"price_change_pct": 10.0},
        },
        {
            "symbol": "TSLA",
            "quant_signal": {"price_change_pct": -5.0},
        },
    ]

    result = run_replay_with_metrics(events)

    assert "metrics" in result
    assert "score_edge" in result["metrics"]
