from fastapi import APIRouter, Request
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.decision_snapshot import DecisionSnapshot

router = APIRouter()


def serialize_decision_list_item(record: DecisionSnapshot) -> dict:
    return {
        "decision_id": record.decision_id,
        "source_signal_id": record.source_signal_id,
        "primary_ticker": record.primary_ticker,
        "decision": record.decision,
        "reason_code": record.reason_code,
        "decision_context": record.decision_context,
        "generated_at": record.generated_at.isoformat().replace("+00:00", "Z"),
    }


@router.get("/decisions/latest")
def get_latest_decisions(request: Request) -> dict:
    with SessionLocal() as session:
        records = session.scalars(
            select(DecisionSnapshot)
            .order_by(desc(DecisionSnapshot.generated_at))
            .limit(50)
        ).all()

    return {
        "data": [serialize_decision_list_item(record) for record in records],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": 50,
            "sort": "generated_at",
            "order": "desc",
        },
        "meta": request.state.meta,
    }
