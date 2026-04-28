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

def evaluate_decision_context(context: dict) -> dict:
    """Evaluate an offline-safe decision context using minimal deterministic rules."""
    news = context.get("news", {})
    quant_signal = context.get("quant_signal", {})

    event_type = news.get("event_type")
    price_change = quant_signal.get("price_change_pct", 0.0)
    relative_volume = quant_signal.get("relative_volume", 0.0)

    if event_type and price_change >= 10.0 and relative_volume >= 2.0:
        return make_decision_result(
            decision=DECISION_ACTIONABLE,
            reason_codes=[
                "NEWS_EVENT_PRESENT",
                "PRICE_CHANGE_STRONG",
                "RELATIVE_VOLUME_STRONG",
            ],
        )

    if event_type:
        return make_decision_result(
            decision=DECISION_WATCHLIST,
            reason_codes=["NEWS_EVENT_PRESENT"],
        )

    return make_decision_result(
        decision=DECISION_NO_TRADE,
        reason_codes=["NO_QUALIFYING_NEWS_EVENT"],
    )

