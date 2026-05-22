import re
from typing import Literal, TypedDict

from app.models.outcome_record import OutcomeRecord


PERFORMANCE_FEEDBACK_FIELDS = (
    "symbol",
    "decision",
    "horizon_minutes",
    "return_pct",
    "max_up_pct",
    "max_down_pct",
    "feedback_label",
    "was_directionally_positive",
    "source_decision_id",
)

Decision = Literal["actionable", "monitor", "neutral"]

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)

SYMBOL_RE = re.compile(r"^[A-Z]{1,10}$")


class PerformanceFeedbackRecord(TypedDict):
    symbol: str
    decision: Decision
    horizon_minutes: int
    return_pct: float
    max_up_pct: float
    max_down_pct: float
    feedback_label: str
    was_directionally_positive: bool
    source_decision_id: str


def _validate_numeric(name: str, value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name}_must_be_numeric")


def validate_performance_feedback(
    record: dict,
) -> PerformanceFeedbackRecord:
    if "feedback_label" in record and record["feedback_label"] not in (
        "positive",
        "negative",
        "neutral",
    ):
        raise ValueError("invalid_feedback_label")

    if tuple(record.keys()) != PERFORMANCE_FEEDBACK_FIELDS:
        raise ValueError("performance_feedback_fields_mismatch")

    symbol = record["symbol"]

    if not isinstance(symbol, str) or not SYMBOL_RE.match(symbol):
        raise ValueError("symbol_must_be_uppercase")

    if record["decision"] not in ("actionable", "monitor", "neutral"):
        raise ValueError("invalid_decision")

    for field in ("return_pct", "max_up_pct", "max_down_pct"):
        _validate_numeric(field, record[field])

    horizon_minutes = record["horizon_minutes"]

    if not isinstance(horizon_minutes, int) or isinstance(horizon_minutes, bool):
        raise ValueError("horizon_minutes_must_be_numeric")

    if horizon_minutes <= 0:
        raise ValueError("horizon_minutes_must_be_positive")

    if not isinstance(record["was_directionally_positive"], bool):
        raise ValueError("was_directionally_positive_must_be_boolean")

    source_decision_id = record["source_decision_id"]

    if (
        not isinstance(source_decision_id, str)
        or not UUID_RE.match(source_decision_id)
    ):
        raise ValueError("source_decision_id_must_be_uuid")

    return record  # type: ignore[return-value]


def build_performance_feedback(
    outcome: OutcomeRecord,
) -> PerformanceFeedbackRecord:
    record = {
        "symbol": outcome["symbol"],
        "decision": outcome["decision"],
        "horizon_minutes": outcome["horizon_minutes"],
        "return_pct": outcome["return_pct"],
        "max_up_pct": outcome["max_up_pct"],
        "max_down_pct": outcome["max_down_pct"],
        "feedback_label": classify_feedback_label(outcome["return_pct"]),
        "was_directionally_positive": outcome["return_pct"] > 0,
        "source_decision_id": outcome["source_decision_id"],
    }

    return validate_performance_feedback(record)


def classify_feedback_label(return_pct: float) -> str:
    _validate_numeric("return_pct", return_pct)

    if return_pct > 0:
        return "positive"

    if return_pct < 0:
        return "negative"

    return "neutral"
