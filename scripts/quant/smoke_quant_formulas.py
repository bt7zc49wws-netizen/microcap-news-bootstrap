from app.quant import (
    acceleration,
    atr,
    atr_pct,
    breakout_pct,
    close_location_value,
    dollar_volume,
    gap_pct,
    intraday_return_pct,
    price_change_pct,
    range_pct,
    relative_volume,
    slope,
    true_range,
    vwap,
    vwap_distance_pct,
)


def main() -> None:
    assert price_change_pct(12.0, 10.0) == 20.0
    assert gap_pct(11.0, 10.0) == 10.0
    assert intraday_return_pct(12.0, 10.0) == 20.0
    assert relative_volume(250_000.0, 100_000.0) == 2.5
    assert dollar_volume(2.5, 100_000.0) == 250_000.0
    assert range_pct(12.0, 9.0, 10.0) == 30.0
    assert close_location_value(10.0, 9.0, 11.0) == 0.0
    assert vwap(1_000_000.0, 200_000.0) == 5.0
    assert vwap_distance_pct(5.5, 5.0) == 10.0
    assert true_range(12.0, 9.0, 10.0) == 3.0
    assert atr([1.0, 2.0, 3.0]) == 2.0
    assert atr_pct(0.5, 10.0) == 5.0
    assert breakout_pct(11.0, 10.0) == 10.0
    assert slope([10.0, 11.0, 12.0, 13.0]) == 1.0
    assert acceleration([10.0, 11.0, 13.0, 16.0, 20.0]) == 2.0
    print("quant formula smoke ok")


if __name__ == "__main__":
    main()
