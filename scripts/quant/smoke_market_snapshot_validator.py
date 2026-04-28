from app.quant import REQUIRED_MARKET_SNAPSHOT_FIELDS, validate_market_snapshot


def main() -> None:
    snapshot = {field: 1.0 for field in REQUIRED_MARKET_SNAPSHOT_FIELDS}
    validated = validate_market_snapshot(snapshot)

    assert validated["current_price"] == 1.0
    assert tuple(validated.keys()) == REQUIRED_MARKET_SNAPSHOT_FIELDS
    print("market snapshot validator smoke ok")


if __name__ == "__main__":
    main()
