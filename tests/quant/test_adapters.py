import pytest

from app.quant.adapters import adapt_market_snapshot


def test_adapt_market_snapshot_returns_validated_snapshot() -> None:
    payload = {
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
        "provider_extra_field": "ignored",
    }

    snapshot = adapt_market_snapshot(payload)

    assert snapshot == {
        "current_price": pytest.approx(12.0),
        "open_price": pytest.approx(11.0),
        "high_price": pytest.approx(13.0),
        "low_price": pytest.approx(10.0),
        "previous_close": pytest.approx(10.0),
        "current_volume": pytest.approx(250_000.0),
        "average_volume": pytest.approx(100_000.0),
        "vwap_value": pytest.approx(10.0),
        "atr_value": pytest.approx(0.6),
        "breakout_level": pytest.approx(10.0),
    }


def test_adapt_market_snapshot_rejects_missing_required_field() -> None:
    with pytest.raises(KeyError):
        adapt_market_snapshot({"current_price": 12.0})
