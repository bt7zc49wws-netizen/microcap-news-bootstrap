import pytest

from app.decision_engine import (
    DECISION_ACTIONABLE,
    DECISION_NO_TRADE,
    DECISION_WATCHLIST,
    DEFAULT_DECISION_THRESHOLDS,
    SUPPORTED_NEWS_EVENT_TYPES,
    VALID_DECISIONS,
    VALID_REASON_CODES,
    REASON_SUPPORTED_NEWS_EVENT,
    REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT,
    REASON_PRICE_CHANGE_STRONG,
    REASON_RELATIVE_VOLUME_STRONG,
    make_decision_result,
    evaluate_decision_context,
)
from app.quant.signals import QUANT_SIGNAL_FIELDS


def _quant_signal(**overrides: float) -> dict[str, float]:
    signal = {field: 1.0 for field in QUANT_SIGNAL_FIELDS}
    signal.update(overrides)
    return signal


def test_valid_decisions_are_canonical() -> None:
    assert VALID_DECISIONS == (
        "no_trade",
        "watchlist",
        "actionable",
    )


def test_make_decision_result_returns_canonical_shape() -> None:
    result = make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=["SUPPORTED_NEWS_EVENT", "QUANT_VOLUME_ACTIVE"],
    )

    assert result == {
        "decision": "watchlist",
        "reason_codes": ["SUPPORTED_NEWS_EVENT", "QUANT_VOLUME_ACTIVE"],
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
            "quant_signal": _quant_signal(price_change_pct=12.0, relative_volume=3.0),
        }
    )

    assert result == {
        "decision": "actionable",
        "reason_codes": [
            "SUPPORTED_NEWS_EVENT",
            "PRICE_CHANGE_STRONG",
            "RELATIVE_VOLUME_STRONG",
        ],
        "symbol": "AAPL",
    }


def test_evaluate_decision_context_returns_watchlist_for_news_without_strong_quant() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {"event_type": "financing"},
            "quant_signal": _quant_signal(price_change_pct=3.0, relative_volume=1.2),
        }
    )

    assert result == {
        "decision": "watchlist",
        "reason_codes": ["SUPPORTED_NEWS_EVENT"],
        "symbol": "AAPL",
    }


def test_evaluate_decision_context_returns_no_trade_without_news_event() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {},
            "quant_signal": _quant_signal(price_change_pct=20.0, relative_volume=5.0),
        }
    )

    assert result == {
        "decision": "no_trade",
        "reason_codes": ["UNSUPPORTED_OR_MISSING_NEWS_EVENT"],
        "symbol": "AAPL",
    }


def test_supported_news_event_types_are_declared() -> None:
    assert "financing" in SUPPORTED_NEWS_EVENT_TYPES
    assert "dilution" in SUPPORTED_NEWS_EVENT_TYPES
    assert "fda" in SUPPORTED_NEWS_EVENT_TYPES


def test_evaluate_decision_context_returns_no_trade_for_unsupported_news_event() -> None:
    result = evaluate_decision_context(
        {
            "symbol": "AAPL",
            "news": {"event_type": "generic_pr"},
            "quant_signal": _quant_signal(price_change_pct=20.0, relative_volume=5.0),
        }
    )

    assert result == {
        "decision": "no_trade",
        "reason_codes": ["UNSUPPORTED_OR_MISSING_NEWS_EVENT"],
        "symbol": "AAPL",
    }


def test_default_decision_thresholds_are_declared() -> None:
    assert DEFAULT_DECISION_THRESHOLDS == {
        "strong_price_change_pct": 10.0,
        "strong_relative_volume": 2.0,
    }


def test_valid_reason_codes_are_canonical() -> None:
    assert VALID_REASON_CODES == (
        "SUPPORTED_NEWS_EVENT",
        "UNSUPPORTED_OR_MISSING_NEWS_EVENT",
        "PRICE_CHANGE_STRONG",
        "RELATIVE_VOLUME_STRONG",
    )
    assert REASON_SUPPORTED_NEWS_EVENT == "SUPPORTED_NEWS_EVENT"
    assert REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT == "UNSUPPORTED_OR_MISSING_NEWS_EVENT"
    assert REASON_PRICE_CHANGE_STRONG == "PRICE_CHANGE_STRONG"
    assert REASON_RELATIVE_VOLUME_STRONG == "RELATIVE_VOLUME_STRONG"


def test_make_decision_result_can_include_symbol() -> None:
    result = make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=["VALID_TEST_REASON"],
        symbol="aapl",
    )

    assert result == {
        "decision": "watchlist",
        "reason_codes": ["VALID_TEST_REASON"],
        "symbol": "AAPL",
    }


def test_make_decision_result_rejects_empty_symbol_when_provided() -> None:
    with pytest.raises(ValueError, match="symbol must not be empty"):
        make_decision_result(
            decision=DECISION_WATCHLIST,
            reason_codes=["VALID_TEST_REASON"],
            symbol="",
        )
