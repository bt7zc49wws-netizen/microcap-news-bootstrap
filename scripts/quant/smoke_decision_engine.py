from app.decision_engine import DECISION_WATCHLIST, make_decision_result


def main() -> None:
    result = make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=["NEWS_EVENT_PRESENT", "QUANT_VOLUME_ACTIVE"],
    )

    assert result["decision"] == "watchlist"
    assert result["reason_codes"] == ["NEWS_EVENT_PRESENT", "QUANT_VOLUME_ACTIVE"]
    print("decision engine smoke ok")


if __name__ == "__main__":
    main()
