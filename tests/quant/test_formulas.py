import pytest

from app.quant.formulas import (
    close_location_value,
    dollar_volume,
    gap_pct,
    intraday_return_pct,
    price_change_pct,
    range_pct,
    relative_volume,
)


def test_price_change_pct() -> None:
    assert price_change_pct(current_price=12.0, previous_close=10.0) == pytest.approx(20.0)
    assert price_change_pct(current_price=8.0, previous_close=10.0) == pytest.approx(-20.0)


def test_gap_pct() -> None:
    assert gap_pct(open_price=11.0, previous_close=10.0) == pytest.approx(10.0)


def test_intraday_return_pct() -> None:
    assert intraday_return_pct(current_price=12.0, open_price=10.0) == pytest.approx(20.0)


def test_relative_volume() -> None:
    assert relative_volume(current_volume=250_000, average_volume=100_000) == pytest.approx(2.5)


def test_dollar_volume() -> None:
    assert dollar_volume(price=2.5, volume=100_000) == pytest.approx(250_000.0)


def test_range_pct() -> None:
    assert range_pct(high_price=12.0, low_price=9.0, reference_price=10.0) == pytest.approx(30.0)


def test_close_location_value() -> None:
    assert close_location_value(close_price=10.0, low_price=9.0, high_price=11.0) == pytest.approx(0.0)
    assert close_location_value(close_price=11.0, low_price=9.0, high_price=11.0) == pytest.approx(1.0)
    assert close_location_value(close_price=9.0, low_price=9.0, high_price=11.0) == pytest.approx(-1.0)


@pytest.mark.parametrize(
    ("func", "kwargs"),
    [
        (price_change_pct, {"current_price": 10.0, "previous_close": 0.0}),
        (gap_pct, {"open_price": 10.0, "previous_close": 0.0}),
        (intraday_return_pct, {"current_price": 10.0, "open_price": 0.0}),
        (relative_volume, {"current_volume": 10.0, "average_volume": 0.0}),
        (range_pct, {"high_price": 11.0, "low_price": 9.0, "reference_price": 0.0}),
        (close_location_value, {"close_price": 10.0, "low_price": 10.0, "high_price": 10.0}),
    ],
)
def test_invalid_denominators_raise_value_error(func, kwargs) -> None:
    with pytest.raises(ValueError):
        func(**kwargs)
