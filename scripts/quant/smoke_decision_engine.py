from app.decision_engine import DECISION_WATCHLIST, evaluate_decision_context, make_decision_result


def main() -> None:
    result = make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=["SUPPORTED_NEWS_EVENT", "QUANT_VOLUME_ACTIVE"],
    )

    assert result["decision"] == "watchlist"
    assert result["reason_codes"] == ["SUPPORTED_NEWS_EVENT", "QUANT_VOLUME_ACTIVE"]

    evaluated = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {"event_type": "financing"},
            "quant_signal": {
                "price_change_pct": 12.0,
                "relative_volume": 3.0,
            },
        }
    )

    assert evaluated["decision"] == "actionable"
    assert evaluated["symbol"] == "AAPL"
    assert evaluated["reason_codes"] == [
        "SUPPORTED_NEWS_EVENT",
        "PRICE_CHANGE_STRONG",
        "RELATIVE_VOLUME_STRONG",
    ]

    print("decision engine smoke ok")


if __name__ == "__main__":
    main()
