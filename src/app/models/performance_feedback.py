from __future__ import annotations

from typing import Literal, TypedDict
from uuid import UUID

from app.models.outcome_record import OutcomeRecord

FeedbackLabel = Literal["positive", "neutral", "negative"]


class PerformanceFeedbackRecord(TypedDict):
    source_decision_id: str
    symbol: str
    decision: str
    horizon_minutes: int
    return_pct: float
    max_up_pct: float
    max_down_pct: float
    was_directionally_positive: bool
    feedback_label: FeedbackLabel


VALID_FEEDBACK_DECISIONS = {"no_trade", "watchlist", "actionable"}
VALID_FEEDBACK_LABELS = {"positive", "neutral", "negative"}
PERFORMANCE_FEEDBACK_FIELDS = (
    "source_decision_id",
    "symbol",
    "decision",
    "horizon_minutes",
    "return_pct",
    "max_up_pct",
    "max_down_pct",
    "was_directionally_positive",
    "feedback_label",
)


def classify_feedback_label(return_pct: float) -> FeedbackLabel:
    if return_pct > 0:
        return "positive"
    if return_pct < 0:
        return "negative"
    return "neutral"


def validate_performance_feedback(record: PerformanceFeedbackRecord) -> PerformanceFeedbackRecord:
    if tuple(record.keys()) != PERFORMANCE_FEEDBACK_FIELDS:
        raise ValueError("performance_feedback_fields_mismatch")
    try:
        UUID(record["source_decision_id"])
    except ValueError as exc:
        raise ValueError("source_decision_id_must_be_uuid") from exc
    if record["symbol"] != record["symbol"].upper() or not record["symbol"]:
        raise ValueError("symbol_must_be_uppercase")
    if record["decision"] not in VALID_FEEDBACK_DECISIONS:
        raise ValueError("invalid_decision")
    if record["horizon_minutes"] <= 0:
        raise ValueError("horizon_minutes_must_be_positive")
    if isinstance(record["return_pct"], bool) or not isinstance(record["return_pct"], int | float):
        raise ValueError("return_pct_must_be_numeric")
    if isinstance(record["max_up_pct"], bool) or not isinstance(record["max_up_pct"], int | float):
        raise ValueError("max_up_pct_must_be_numeric")
    if isinstance(record["max_down_pct"], bool) or not isinstance(record["max_down_pct"], int | float):
        raise ValueError("max_down_pct_must_be_numeric")
    if record["feedback_label"] not in VALID_FEEDBACK_LABELS:
        raise ValueError("invalid_feedback_label")
    return record


def build_performance_feedback(outcome: OutcomeRecord) -> PerformanceFeedbackRecord:
    return validate_performance_feedback(
        {
            "source_decision_id": outcome["source_decision_id"],
            "symbol": outcome["symbol"],
            "decision": outcome["decision"],
            "horizon_minutes": outcome["horizon_minutes"],
            "return_pct": outcome["return_pct"],
            "max_up_pct": outcome["max_up_pct"],
            "max_down_pct": outcome["max_down_pct"],
            "was_directionally_positive": outcome["return_pct"] > 0,
            "feedback_label": classify_feedback_label(outcome["return_pct"]),
        }
    )
