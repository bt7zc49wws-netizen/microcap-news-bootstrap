from app.analytics.buckets import analyze_buckets


def test_analyze_buckets() -> None:
    events = [
        {
            "output": {
                "label": 1.0,
                "decision": {
                    "decision_context": {
                        "decision_score": 0.9,
                    }
                },
            }
        }
    ]

    result = analyze_buckets(events)

    assert result["HIGH"]["avg_return"] == 1.0


def test_bucket_monotonicity() -> None:
    events = [
        {"label": -1.0, "output": {"decision": {"decision_context": {"decision_score": 0.1}}}},
        {"label": 1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
    ]

    result = analyze_buckets(events)

    assert result["LOW"]["samples"] == 1
    assert result["HIGH"]["samples"] == 1
    assert result["monotonic"] is True


def test_bucket_stddev() -> None:
    events = [
        {"label": 1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
        {"label": -1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
    ]

    result = analyze_buckets(events)

    assert result["HIGH"]["samples"] == 2
    assert result["HIGH"]["stddev"] > 0.0


def test_bucket_win_rate() -> None:
    events = [
        {"label": 1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
        {"label": 1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
        {"label": -1.0, "output": {"decision": {"decision_context": {"decision_score": 0.9}}}},
    ]

    result = analyze_buckets(events)

    assert result["HIGH"]["samples"] == 3
    assert result["HIGH"]["win_rate"] == 2 / 3
