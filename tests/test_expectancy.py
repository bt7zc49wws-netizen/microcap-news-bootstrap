from app.replay.analytics_replay import run_replay_with_metrics


def test_expectancy_metrics_exist() -> None:
    events = [
        {
            "symbol": "TEST",
            "signal": "BUY",
            "label": 1.0,
        }
    ]

    result = run_replay_with_metrics(events)

    assert "metrics" in result


def test_replay_includes_bucket_metrics() -> None:
    events = [
        {
            "symbol": "TEST",
            "signal": "BUY",
            "label": 1.0,
        }
    ]

    result = run_replay_with_metrics(events)

    assert "bucket_metrics" in result
    assert "HIGH" in result["bucket_metrics"]


def test_quality_snapshot_exists() -> None:
    events = [
        {
            "symbol": "TEST",
            "signal": "BUY",
            "label": 1.0,
        }
    ]

    result = run_replay_with_metrics(events)

    assert "quality_snapshot" in result
    assert "monotonic" in result["quality_snapshot"]
    assert "high_bucket_avg_return" in result["quality_snapshot"]
    assert "high_bucket_samples" in result["quality_snapshot"]


def test_expectancy_quality_exists() -> None:
    events = [
        {
            "symbol": "TEST",
            "signal": "BUY",
            "label": 1.0,
        }
    ]

    result = run_replay_with_metrics(events)

    assert "expectancy_quality" in result
    assert isinstance(result["expectancy_quality"], float)
