from app.quant import (
    adapt_stooq_market_snapshot,
    build_quant_signal_from_snapshot,
    enrich_stooq_market_payload,
)
from app.services.providers.market_data.client import normalize_stooq_ohlcv_rows


def main() -> None:
    stooq_rows = [
        {"Open": "9", "High": "10", "Low": "8", "Close": "9.5", "Volume": "100"},
        {"Open": "10", "High": "12", "Low": "9", "Close": "11", "Volume": "200"},
        {"Open": "11", "High": "13", "Low": "10", "Close": "12", "Volume": "300"},
        {"Open": "12", "High": "14", "Low": "11", "Close": "13", "Volume": "999"},
    ]

    ohlcv_rows = normalize_stooq_ohlcv_rows(stooq_rows)
    payload = enrich_stooq_market_payload(
        ohlcv_rows,
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
    print("stooq payload to quant signal smoke ok")


if __name__ == "__main__":
    main()
