"""Offline-safe decision engine skeleton.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- no order generation
"""

from __future__ import annotations

DECISION_NO_TRADE = "no_trade"
DECISION_WATCHLIST = "watchlist"
DECISION_ACTIONABLE = "actionable"

VALID_DECISIONS = (
    DECISION_NO_TRADE,
    DECISION_WATCHLIST,
    DECISION_ACTIONABLE,
)


def make_decision_result(
    *,
    decision: str,
    reason_codes: list[str],
) -> dict:
    """Build a canonical decision result."""
    if decision not in VALID_DECISIONS:
        raise ValueError(f"invalid decision: {decision}")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")

    return {
        "decision": decision,
        "reason_codes": reason_codes,
    }
