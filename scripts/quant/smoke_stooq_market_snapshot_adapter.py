from app.quant import STOOQ_MARKET_SNAPSHOT_FIELD_MAP, adapt_stooq_market_snapshot


def main() -> None:
    payload = {
        "close": 12.0,
        "open": 11.0,
        "high": 13.0,
        "low": 10.0,
        "previous_close": 10.0,
        "volume": 250_000.0,
        "average_volume": 100_000.0,
        "vwap": 10.0,
        "atr": 0.6,
        "breakout_level": 10.0,
        "stooq_extra": "ignored",
    }

    snapshot = adapt_stooq_market_snapshot(payload)

    assert STOOQ_MARKET_SNAPSHOT_FIELD_MAP["current_price"] == "close"
    assert snapshot["current_price"] == 12.0
    assert snapshot["current_volume"] == 250_000.0
    assert "stooq_extra" not in snapshot
    print("stooq market snapshot adapter smoke ok")


if __name__ == "__main__":
    main()
