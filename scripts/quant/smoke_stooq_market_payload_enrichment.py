from app.quant import enrich_stooq_market_payload


def main() -> None:
    rows = [
        {"open": 9.0, "high": 10.0, "low": 8.0, "close": 9.5, "volume": 100.0},
        {"open": 10.0, "high": 12.0, "low": 9.0, "close": 11.0, "volume": 200.0},
        {"open": 11.0, "high": 13.0, "low": 10.0, "close": 12.0, "volume": 300.0},
        {"open": 12.0, "high": 14.0, "low": 11.0, "close": 13.0, "volume": 999.0},
    ]

    payload = enrich_stooq_market_payload(
        rows,
        average_volume_lookback=3,
        vwap_lookback=3,
        atr_lookback=3,
        breakout_lookback=3,
    )

    assert payload["close"] == 13.0
    assert payload["previous_close"] == 12.0
    assert payload["average_volume"] == 200.0
    assert payload["breakout_level"] == 13.0
    print("stooq market payload enrichment smoke ok")


if __name__ == "__main__":
    main()
