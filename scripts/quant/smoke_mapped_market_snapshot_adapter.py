from app.quant import adapt_mapped_market_snapshot


def main() -> None:
    payload = {
        "last": 12.0,
        "open": 11.0,
        "high": 13.0,
        "low": 10.0,
        "prev_close": 10.0,
        "volume": 250_000.0,
        "avg_volume": 100_000.0,
        "vwap": 10.0,
        "atr": 0.6,
        "breakout": 10.0,
        "provider_extra_field": "ignored",
    }

    field_map = {
        "current_price": "last",
        "open_price": "open",
        "high_price": "high",
        "low_price": "low",
        "previous_close": "prev_close",
        "current_volume": "volume",
        "average_volume": "avg_volume",
        "vwap_value": "vwap",
        "atr_value": "atr",
        "breakout_level": "breakout",
    }

    snapshot = adapt_mapped_market_snapshot(payload, field_map)

    assert snapshot["current_price"] == 12.0
    assert snapshot["current_volume"] == 250_000.0
    assert "provider_extra_field" not in snapshot
    print("mapped market snapshot adapter smoke ok")


if __name__ == "__main__":
    main()
