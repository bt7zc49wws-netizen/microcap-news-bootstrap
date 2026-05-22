from app.analytics.buckets import analyze_buckets


def test_bucket_analysis_runs() -> None:
    events = [
        {
            "output": {
                "decision": {
                    "decision_context": {"decision_score": 0.1}
                }
            },
            "label": 1.0,
        },
        {
            "output": {
                "decision": {
                    "decision_context": {"decision_score": 0.8}
                }
            },
            "label": 2.0,
        },
    ]

    result = analyze_buckets(events)

    assert "LOW" in result
    assert "HIGH" in result
