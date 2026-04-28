from app.quant import adapt_market_snapshot


def main() -> None:
    snapshot = adapt_market_snapshot(
        {
            "current_price": 12.0,
            "open_price": 11.0,
            "high_price": 13.0,
            "low_price": 10.0,
            "previous_close": 10.0,
            "current_volume": 250_000.0,
            "average_volume": 100_000.0,
            "vwap_value": 10.0,
            "atr_value": 0.6,
            "breakout_level": 10.0,
            "provider_extra_field": "ignored",
        }
    )

    assert snapshot["current_price"] == 12.0
    assert snapshot["current_volume"] == 250_000.0
    assert "provider_extra_field" not in snapshot
    print("market snapshot adapter smoke ok")


if __name__ == "__main__":
    main()
