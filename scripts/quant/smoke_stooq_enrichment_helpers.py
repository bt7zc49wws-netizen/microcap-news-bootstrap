from app.quant import (
    derive_atr,
    derive_average_volume,
    derive_breakout_level,
    derive_previous_close,
    derive_vwap,
)


def main() -> None:
    rows = [
        {"open": 9.0, "high": 10.0, "low": 8.0, "close": 9.5, "volume": 100.0},
        {"open": 10.0, "high": 12.0, "low": 9.0, "close": 11.0, "volume": 200.0},
        {"open": 11.0, "high": 13.0, "low": 10.0, "close": 12.0, "volume": 300.0},
        {"open": 12.0, "high": 14.0, "low": 11.0, "close": 13.0, "volume": 999.0},
    ]

    assert derive_previous_close(rows) == 12.0
    assert derive_average_volume(rows, lookback=3) == 200.0
    assert derive_vwap(rows, lookback=3) > 0
    assert derive_atr(rows, lookback=3) > 0
    assert derive_breakout_level(rows, lookback=3) == 13.0
    print("stooq enrichment helpers smoke ok")


if __name__ == "__main__":
    main()
