from app.quant import build_quant_signal


def main() -> None:
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

    assert signal["price_change_pct"] == 20.0
    assert signal["relative_volume"] == 2.5
    assert signal["dollar_volume"] == 3_000_000.0
    assert signal["atr_pct"] == 5.0
    print("quant signal builder smoke ok")


if __name__ == "__main__":
    main()
