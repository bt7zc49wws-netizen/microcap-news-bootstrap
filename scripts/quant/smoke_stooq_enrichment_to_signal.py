from app.quant import (
    adapt_stooq_market_snapshot,
    build_quant_signal_from_snapshot,
    enrich_stooq_market_payload,
)


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
    snapshot = adapt_stooq_market_snapshot(payload)
    signal = build_quant_signal_from_snapshot(snapshot)

    assert signal["price_change_pct"] > 0
    assert signal["relative_volume"] > 1
    assert signal["breakout_pct"] == 0.0
    print("stooq enrichment to quant signal smoke ok")


if __name__ == "__main__":
    main()
