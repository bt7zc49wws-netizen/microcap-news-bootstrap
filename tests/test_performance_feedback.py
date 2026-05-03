import pytest

from app.models.performance_feedback import (
    PERFORMANCE_FEEDBACK_FIELDS,
    build_performance_feedback,
    classify_feedback_label,
    validate_performance_feedback,
)


def _outcome(**overrides: object) -> dict:
    outcome = {
        "source_decision_id": "11111111-1111-4111-8111-111111111111",
        "symbol": "AAPL",
        "decision": "actionable",
        "measured_at_utc": "2026-05-01T18:00:00Z",
        "horizon_minutes": 60,
        "reference_price": 10.0,
        "observed_price": 11.0,
        "return_pct": 10.0,
        "max_up_pct": 12.0,
        "max_down_pct": -2.0,
    }
    outcome.update(overrides)
    return outcome


def test_classify_feedback_label() -> None:
    assert classify_feedback_label(1.0) == "positive"
    assert classify_feedback_label(0.0) == "neutral"
    assert classify_feedback_label(-1.0) == "negative"


def test_build_performance_feedback_from_outcome() -> None:
    record = build_performance_feedback(_outcome())

    assert tuple(record.keys()) == PERFORMANCE_FEEDBACK_FIELDS
    assert record["source_decision_id"] == "11111111-1111-4111-8111-111111111111"
    assert record["symbol"] == "AAPL"
    assert record["decision"] == "actionable"
    assert record["horizon_minutes"] == 60
    assert record["return_pct"] == 10.0
    assert record["max_up_pct"] == 12.0
    assert record["max_down_pct"] == -2.0
    assert record["was_directionally_positive"] is True
    assert record["feedback_label"] == "positive"


def test_validate_performance_feedback_rejects_field_drift() -> None:
    record = build_performance_feedback(_outcome())
    record["extra_field"] = "must not leak"

    with pytest.raises(ValueError, match="performance_feedback_fields_mismatch"):
        validate_performance_feedback(record)


def test_validate_performance_feedback_rejects_non_uuid_source_decision_id() -> None:
    record = build_performance_feedback(_outcome())
    record["source_decision_id"] = "decision-1"

    with pytest.raises(ValueError, match="source_decision_id_must_be_uuid"):
        validate_performance_feedback(record)
