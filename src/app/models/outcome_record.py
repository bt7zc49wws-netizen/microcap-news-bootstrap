from __future__ import annotations

from typing import TypedDict


class OutcomeRecord(TypedDict):
    source_decision_id: str
    symbol: str
    decision: str
    measured_at_utc: str
    horizon_minutes: int
    reference_price: float
    observed_price: float
    return_pct: float
    max_up_pct: float
    max_down_pct: float


VALID_OUTCOME_DECISIONS = {"no_trade", "watchlist", "actionable"}
OUTCOME_RECORD_FIELDS = (
    "source_decision_id",
    "symbol",
    "decision",
    "measured_at_utc",
    "horizon_minutes",
    "reference_price",
    "observed_price",
    "return_pct",
    "max_up_pct",
    "max_down_pct",
)


def validate_outcome_record(record: OutcomeRecord) -> OutcomeRecord:
    if tuple(record.keys()) != OUTCOME_RECORD_FIELDS:
        raise ValueError("outcome_record_fields_mismatch")
    if not record["source_decision_id"]:
        raise ValueError("source_decision_id_required")
    if record["symbol"] != record["symbol"].upper() or not record["symbol"]:
        raise ValueError("symbol_must_be_uppercase")
    if record["decision"] not in VALID_OUTCOME_DECISIONS:
        raise ValueError("invalid_decision")
    if record["horizon_minutes"] <= 0:
        raise ValueError("horizon_minutes_must_be_positive")
    if record["reference_price"] <= 0 or record["observed_price"] <= 0:
        raise ValueError("prices_must_be_positive")
    return record


def calculate_return_pct(reference_price: float, observed_price: float) -> float:
    if reference_price <= 0 or observed_price <= 0:
        raise ValueError("prices_must_be_positive")
    return ((observed_price - reference_price) / reference_price) * 100.0
