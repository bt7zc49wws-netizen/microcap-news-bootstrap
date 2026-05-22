from app.replay.replay_engine import run_replay


def test_replay_runs_end_to_end() -> None:
    event = {
        "symbol": "AAPL",
        "news": {"event_type": "generic_pr"},
        "quant_signal": {
            "price_change_pct": 10.0,
            "relative_volume": 2.0,
        },
    }

    result = run_replay(event)

    assert "input" in result
    assert "output" in result
    assert "decision" in result["output"]
