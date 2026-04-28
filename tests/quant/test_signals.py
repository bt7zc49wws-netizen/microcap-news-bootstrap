import pytest

from app.quant.signals import build_quant_signal


def test_build_quant_signal_returns_canonical_fields() -> None:
    signal = build_quant_signal(
        current_price=12.0,
        open_price=11.0,
        high_price=13.0,
        low_price=10.0,
        previous_close=10.0,
        current_volume=250_000.0,
        average_volume=100_000.0,
        vwap_value=10.0,
        atr_value=0.6,
        breakout_level=10.0,
    )

    assert signal == {
        "price_change_pct": pytest.approx(20.0),
        "gap_pct": pytest.approx(10.0),
        "intraday_return_pct": pytest.approx(9.0909090909),
        "relative_volume": pytest.approx(2.5),
        "dollar_volume": pytest.approx(3_000_000.0),
        "range_pct": pytest.approx(30.0),
        "close_location_value": pytest.approx(0.3333333333),
        "vwap_distance_pct": pytest.approx(20.0),
        "atr_pct": pytest.approx(5.0),
        "breakout_pct": pytest.approx(20.0),
    }


def test_build_quant_signal_raises_for_invalid_denominator() -> None:
    with pytest.raises(ValueError):
        build_quant_signal(
            current_price=12.0,
            open_price=11.0,
            high_price=13.0,
            low_price=10.0,
            previous_close=0.0,
            current_volume=250_000.0,
            average_volume=100_000.0,
            vwap_value=10.0,
            atr_value=0.6,
            breakout_level=10.0,
        )
