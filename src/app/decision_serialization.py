"""Decision snapshot serialization helpers."""

from __future__ import annotations

from app.json_utils import loads_json_list, loads_json_object
from app.models.decision_snapshot import DecisionSnapshot


def serialize_decision_metadata(record: DecisionSnapshot) -> dict:
    return {
        "decision_id": record.decision_id,
        "primary_ticker": record.primary_ticker,
        "decision": record.decision,
        "rule_id": record.rule_id,
        "rule_version": record.rule_version,
        "reason_code": record.reason_code,
        "reason_label": record.reason_label,
        "generated_at": record.generated_at.isoformat().replace("+00:00", "Z"),
    }


def serialize_decision_detail_payload(record: DecisionSnapshot) -> dict:
    data = serialize_decision_metadata(record)

    data.update(
        {
            "source_signal_id": record.source_signal_id,
            "decision_summary": record.decision_summary,
            "decision_context": loads_json_object(record.decision_context),
            "confidence": record.confidence,
            "risk_flags": loads_json_list(record.risk_flags),
        }
    )

    return data
