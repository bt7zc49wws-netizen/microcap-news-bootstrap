import pytest

from app.quant.snapshot import REQUIRED_MARKET_SNAPSHOT_FIELDS, validate_market_snapshot


def test_validate_market_snapshot_accepts_required_numeric_fields() -> None:
    snapshot = {
        "current_price": 12.0,
        "open_price": 11.0,
        "high_price": 13.0,
        "low_price": 10.0,
        "previous_close": 10.0,
        "current_volume": 250_000,
        "average_volume": 100_000,
        "vwap_value": 10.0,
        "atr_value": 0.6,
        "breakout_level": 10.0,
    }

    validated = validate_market_snapshot(snapshot)

    assert tuple(validated.keys()) == REQUIRED_MARKET_SNAPSHOT_FIELDS
    assert validated["current_volume"] == pytest.approx(250_000.0)


def test_validate_market_snapshot_rejects_missing_required_field() -> None:
    snapshot = {field: 1.0 for field in REQUIRED_MARKET_SNAPSHOT_FIELDS}
    snapshot.pop("current_price")

    with pytest.raises(ValueError, match="missing required market snapshot fields"):
        validate_market_snapshot(snapshot)


def test_validate_market_snapshot_rejects_non_numeric_value() -> None:
    snapshot = {field: 1.0 for field in REQUIRED_MARKET_SNAPSHOT_FIELDS}
    snapshot["current_price"] = "12.0"

    with pytest.raises(ValueError, match="current_price must be numeric"):
        validate_market_snapshot(snapshot)


def test_validate_market_snapshot_drops_extra_fields() -> None:
    snapshot = {field: 1.0 for field in REQUIRED_MARKET_SNAPSHOT_FIELDS}
    snapshot["raw_provider_payload"] = {"secret": "must not leak"}

    validated = validate_market_snapshot(snapshot)

    assert tuple(validated.keys()) == REQUIRED_MARKET_SNAPSHOT_FIELDS
    assert "raw_provider_payload" not in validated
