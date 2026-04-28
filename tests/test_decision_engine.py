import pytest

from app.decision_engine import (
    DECISION_ACTIONABLE,
    DECISION_NO_TRADE,
    DECISION_WATCHLIST,
    VALID_DECISIONS,
    make_decision_result,
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
