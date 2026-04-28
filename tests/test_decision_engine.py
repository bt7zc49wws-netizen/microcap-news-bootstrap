import pytest

from app.decision_engine import (
    DECISION_ACTIONABLE,
    DECISION_NO_TRADE,
    DECISION_WATCHLIST,
    VALID_DECISIONS,
    make_decision_result,
    evaluate_decision_context,
)


def test_valid_decisions_are_canonical() -> None:
    assert VALID_DECISIONS == (
        "no_trade",
        "watchlist",
        "actionable",
    )


def test_make_decision_result_returns_canonical_shape() -> None:
    result = make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=["NEWS_EVENT_PRESENT", "QUANT_VOLUME_ACTIVE"],
    )

    assert result == {
        "decision": "watchlist",
        "reason_codes": ["NEWS_EVENT_PRESENT", "QUANT_VOLUME_ACTIVE"],
    }


@pytest.mark.parametrize(
    "decision",
    [DECISION_NO_TRADE, DECISION_WATCHLIST, DECISION_ACTIONABLE],
)
def test_make_decision_result_accepts_all_valid_decisions(decision: str) -> None:
    result = make_decision_result(
        decision=decision,
        reason_codes=["VALID_TEST_REASON"],
    )

    assert result["decision"] == decision


def test_make_decision_result_rejects_invalid_decision() -> None:
    with pytest.raises(ValueError, match="invalid decision"):
        make_decision_result(
            decision="trade",
            reason_codes=["INVALID_LEGACY_DECISION"],
        )


def test_make_decision_result_rejects_empty_reason_codes() -> None:
    with pytest.raises(ValueError, match="reason_codes must not be empty"):
        make_decision_result(
            decision=DECISION_NO_TRADE,
            reason_codes=[],
        )


def test_evaluate_decision_context_returns_actionable_for_news_and_strong_quant() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {"event_type": "financing"},
            "quant_signal": {
                "price_change_pct": 12.0,
                "relative_volume": 3.0,
            },
        }
    )

    assert result == {
        "decision": "actionable",
        "reason_codes": [
            "NEWS_EVENT_PRESENT",
            "PRICE_CHANGE_STRONG",
            "RELATIVE_VOLUME_STRONG",
        ],
    }


def test_evaluate_decision_context_returns_watchlist_for_news_without_strong_quant() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {"event_type": "financing"},
            "quant_signal": {
                "price_change_pct": 3.0,
                "relative_volume": 1.2,
            },
        }
    )

    assert result == {
        "decision": "watchlist",
        "reason_codes": ["NEWS_EVENT_PRESENT"],
    }


def test_evaluate_decision_context_returns_no_trade_without_news_event() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {},
            "quant_signal": {
                "price_change_pct": 20.0,
                "relative_volume": 5.0,
            },
        }
    )

    assert result == {
        "decision": "no_trade",
        "reason_codes": ["NO_QUALIFYING_NEWS_EVENT"],
    }
