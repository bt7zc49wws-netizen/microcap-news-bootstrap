from app.replay.batch_replay import run_batch_replay


def test_batch_replay_summary() -> None:
    events = [
        {
            "symbol": "AAPL",
            "news": {"event_type": "generic_pr"},
            "quant_signal": {"price_change_pct": 5.0, "relative_volume": 2.0},
        },
        {
            "symbol": "TSLA",
            "news": {},
            "quant_signal": {"price_change_pct": -10.0, "relative_volume": 1.0},
        },
    ]

    result = run_batch_replay(events)

    assert result["summary"]["total"] == 2
