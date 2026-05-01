import pytest

from app.models.outcome_record import (
    OUTCOME_RECORD_FIELDS,
    build_outcome_record,
    calculate_max_down_pct,
    calculate_max_up_pct,
    calculate_return_pct,
    validate_outcome_record,
)


def _record(**overrides: object) -> dict:
    record = {
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
    record.update(overrides)
    return record


def test_validate_outcome_record_accepts_canonical_record() -> None:
    record = _record()

    assert validate_outcome_record(record) == record
    assert tuple(record.keys()) == OUTCOME_RECORD_FIELDS


def test_validate_outcome_record_rejects_field_drift() -> None:
    record = _record(extra_field="must not leak")

    with pytest.raises(ValueError, match="outcome_record_fields_mismatch"):
        validate_outcome_record(record)


def test_validate_outcome_record_rejects_lowercase_symbol() -> None:
    with pytest.raises(ValueError, match="symbol_must_be_uppercase"):
        validate_outcome_record(_record(symbol="aapl"))


def test_validate_outcome_record_rejects_invalid_decision() -> None:
    with pytest.raises(ValueError, match="invalid_decision"):
        validate_outcome_record(_record(decision="trade"))


def test_validate_outcome_record_rejects_non_positive_horizon() -> None:
    with pytest.raises(ValueError, match="horizon_minutes_must_be_positive"):
        validate_outcome_record(_record(horizon_minutes=0))


def test_validate_outcome_record_rejects_non_positive_prices() -> None:
    with pytest.raises(ValueError, match="prices_must_be_positive"):
        validate_outcome_record(_record(reference_price=0.0))


def test_calculate_return_pct() -> None:
    assert calculate_return_pct(10.0, 11.0) == pytest.approx(10.0)
    assert calculate_return_pct(10.0, 9.0) == pytest.approx(-10.0)


def test_calculate_return_pct_rejects_non_positive_prices() -> None:
    with pytest.raises(ValueError, match="prices_must_be_positive"):
        calculate_return_pct(0.0, 11.0)


def test_build_outcome_record_calculates_return_and_validates_shape() -> None:
    record = build_outcome_record(
        source_decision_id="11111111-1111-4111-8111-111111111111",
        symbol="AAPL",
        decision="actionable",
        measured_at_utc="2026-05-01T18:00:00Z",
        horizon_minutes=60,
        reference_price=10.0,
        observed_price=11.0,
        max_up_pct=12.0,
        max_down_pct=-2.0,
    )

    assert tuple(record.keys()) == OUTCOME_RECORD_FIELDS
    assert record["return_pct"] == pytest.approx(10.0)


def test_build_outcome_record_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="symbol_must_be_uppercase"):
        build_outcome_record(
            source_decision_id="11111111-1111-4111-8111-111111111111",
            symbol="aapl",
            decision="actionable",
            measured_at_utc="2026-05-01T18:00:00Z",
            horizon_minutes=60,
            reference_price=10.0,
            observed_price=11.0,
            max_up_pct=12.0,
            max_down_pct=-2.0,
        )


def test_validate_outcome_record_rejects_non_uuid_source_decision_id() -> None:
    with pytest.raises(ValueError, match="source_decision_id_must_be_uuid"):
        validate_outcome_record(_record(source_decision_id="decision-1"))


def test_calculate_max_up_pct() -> None:
    assert calculate_max_up_pct(10.0, 12.0) == pytest.approx(20.0)


def test_calculate_max_down_pct() -> None:
    assert calculate_max_down_pct(10.0, 8.0) == pytest.approx(-20.0)


def test_calculate_max_movement_pct_rejects_non_positive_prices() -> None:
    with pytest.raises(ValueError, match="prices_must_be_positive"):
        calculate_max_up_pct(0.0, 12.0)
    with pytest.raises(ValueError, match="prices_must_be_positive"):
        calculate_max_down_pct(10.0, 0.0)
