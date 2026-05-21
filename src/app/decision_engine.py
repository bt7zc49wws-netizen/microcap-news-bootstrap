"""Offline-safe decision engine skeleton.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- no order generation
"""

from __future__ import annotations
from app.risk_flags import build_risk_flags

DECISION_NO_TRADE = "no_trade"
DECISION_WATCHLIST = "watchlist"
DECISION_ACTIONABLE = "actionable"

VALID_DECISIONS = (
    DECISION_NO_TRADE,
    DECISION_WATCHLIST,
    DECISION_ACTIONABLE,
)

SUPPORTED_NEWS_EVENT_TYPES = (
    "financing",
    "dilution",
    "offering",
    "clinical",
    "fda",
    "earnings",
    "merger",
    "contract",
)

DEFAULT_DECISION_THRESHOLDS = {
    "strong_price_change_pct": 10.0,
    "strong_relative_volume": 2.0,
}

REASON_SUPPORTED_NEWS_EVENT = "SUPPORTED_NEWS_EVENT"
REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT = "UNSUPPORTED_OR_MISSING_NEWS_EVENT"
REASON_PRICE_CHANGE_STRONG = "PRICE_CHANGE_STRONG"
REASON_RELATIVE_VOLUME_STRONG = "RELATIVE_VOLUME_STRONG"

VALID_REASON_CODES = (
    REASON_SUPPORTED_NEWS_EVENT,
    REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT,
    REASON_PRICE_CHANGE_STRONG,
    REASON_RELATIVE_VOLUME_STRONG,
)


def make_decision_result(
    *,
    decision: str,
    reason_codes: list[str],
    symbol: str | None = None,
    confidence: float | None = None,
    risk_flags: list[str] | None = None,
) -> dict:
    """Build a canonical decision result."""
    if decision not in VALID_DECISIONS:
        raise ValueError(f"invalid decision: {decision}")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")

    result = {
        "decision": decision,
        "reason_codes": reason_codes,
    }

    if confidence is not None:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        result["confidence"] = confidence

    if risk_flags is not None:
        result["risk_flags"] = sorted(set(str(flag) for flag in risk_flags if str(flag).strip()))

    if symbol is not None:
        normalized_symbol = str(symbol).strip()
        if not normalized_symbol:
            raise ValueError("symbol must not be empty")
        result["symbol"] = normalized_symbol.upper()

    return result


def evaluate_decision_context(context: dict) -> dict:
    """Evaluate an offline-safe decision context using minimal deterministic rules."""
    news = context.get("news", {})
    quant_signal = context.get("quant_signal", {})

    event_type = news.get("event_type")
    price_change = quant_signal.get("price_change_pct", 0.0)
    relative_volume = quant_signal.get("relative_volume", 0.0)

    symbol = context.get("symbol")

    risk_flags = build_risk_flags(
        event_type=event_type,
        price_change=price_change,
        relative_volume=relative_volume,
    )

    if event_type in {"offering", "dilution"}:
        risk_flags.append("dilution_risk")

    if event_type == "financing":
        risk_flags.append("financing_risk")

    if event_type not in SUPPORTED_NEWS_EVENT_TYPES:
        return make_decision_result(
            decision=DECISION_NO_TRADE,
            reason_codes=[REASON_UNSUPPORTED_OR_MISSING_NEWS_EVENT],
            symbol=symbol,
            confidence=0.1,
            risk_flags=risk_flags,
        )

    if price_change >= DEFAULT_DECISION_THRESHOLDS["strong_price_change_pct"] and relative_volume >= DEFAULT_DECISION_THRESHOLDS["strong_relative_volume"]:
        return make_decision_result(
            decision=DECISION_ACTIONABLE,
            reason_codes=[
                REASON_SUPPORTED_NEWS_EVENT,
                REASON_PRICE_CHANGE_STRONG,
                REASON_RELATIVE_VOLUME_STRONG,
            ],
            symbol=symbol,
            confidence=0.9,
            risk_flags=risk_flags,
        )

    return make_decision_result(
        decision=DECISION_WATCHLIST,
        reason_codes=[REASON_SUPPORTED_NEWS_EVENT],
        symbol=symbol,
        confidence=0.5,
        risk_flags=risk_flags,
    )

