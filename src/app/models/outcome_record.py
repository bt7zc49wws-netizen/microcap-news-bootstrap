import re
import uuid
from typing import Literal, TypedDict


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


Decision = Literal["actionable", "monitor", "neutral"]

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)

SYMBOL_RE = re.compile(r"^[A-Z]{1,10}$")


class OutcomeRecord(TypedDict):
    source_decision_id: str
    symbol: str
    decision: Decision
    measured_at_utc: str
    horizon_minutes: int
    reference_price: float
    observed_price: float
    return_pct: float
    max_up_pct: float
    max_down_pct: float


def _validate_numeric(name: str, value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name}_must_be_numeric")


def _calculate_pct(reference_price: float, observed_price: float) -> float:
    _validate_numeric("reference_price", reference_price)
    _validate_numeric("observed_price", observed_price)

    if reference_price <= 0 or observed_price <= 0:
        raise ValueError("prices_must_be_positive")

    return ((observed_price - reference_price) / reference_price) * 100.0


def calculate_return_pct(reference_price: float, observed_price: float) -> float:
    return _calculate_pct(reference_price, observed_price)


def calculate_max_up_pct(reference_price: float, high_price: float) -> float:
    return _calculate_pct(reference_price, high_price)


def calculate_max_down_pct(reference_price: float, low_price: float) -> float:
    return _calculate_pct(reference_price, low_price)


def validate_outcome_record(record: dict) -> OutcomeRecord:
    if tuple(record.keys()) != OUTCOME_RECORD_FIELDS:
        raise ValueError("outcome_record_fields_mismatch")

    symbol = record["symbol"]

    if not isinstance(symbol, str) or not SYMBOL_RE.match(symbol):
        raise ValueError("symbol_must_be_uppercase")

    if record["decision"] not in ("actionable", "monitor", "neutral"):
        raise ValueError("invalid_decision")

    for field in (
        "reference_price",
        "observed_price",
        "max_up_pct",
        "max_down_pct",
        "return_pct",
    ):
        _validate_numeric(field, record[field])

    if record["reference_price"] <= 0 or record["observed_price"] <= 0:
        raise ValueError("prices_must_be_positive")

    horizon_minutes = record["horizon_minutes"]

    if not isinstance(horizon_minutes, int) or isinstance(horizon_minutes, bool):
        raise ValueError("horizon_minutes_must_be_numeric")

    if horizon_minutes <= 0:
        raise ValueError("horizon_minutes_must_be_positive")

    source_decision_id = record["source_decision_id"]

    if (
        not isinstance(source_decision_id, str)
        or not UUID_RE.match(source_decision_id)
    ):
        raise ValueError("source_decision_id_must_be_uuid")

    return record  # type: ignore[return-value]


def build_outcome_record(**kwargs) -> OutcomeRecord:
    if "return_pct" in kwargs:
        return_pct = kwargs["return_pct"]
    else:
        return_pct = calculate_return_pct(
            kwargs["reference_price"],
            kwargs["observed_price"],
        )

    record = {
        "source_decision_id": kwargs.get(
            "source_decision_id",
            str(uuid.uuid4()),
        ),
        "symbol": kwargs["symbol"],
        "decision": kwargs["decision"],
        "measured_at_utc": kwargs["measured_at_utc"],
        "horizon_minutes": kwargs["horizon_minutes"],
        "reference_price": kwargs["reference_price"],
        "observed_price": kwargs["observed_price"],
        "return_pct": return_pct,
        "max_up_pct": kwargs["max_up_pct"],
        "max_down_pct": kwargs["max_down_pct"],
    }

    return validate_outcome_record(record)


def build_outcome_record_from_prices(**kwargs) -> OutcomeRecord:
    reference_price = kwargs["reference_price"]

    return build_outcome_record(
        source_decision_id=kwargs.get(
            "source_decision_id",
            str(uuid.uuid4()),
        ),
        symbol=kwargs["symbol"],
        decision=kwargs["decision"],
        measured_at_utc=kwargs["measured_at_utc"],
        horizon_minutes=kwargs["horizon_minutes"],
        reference_price=reference_price,
        observed_price=kwargs["observed_price"],
        max_up_pct=calculate_max_up_pct(
            reference_price,
            kwargs["high_price"],
        ),
        max_down_pct=calculate_max_down_pct(
            reference_price,
            kwargs["low_price"],
        ),
    )
