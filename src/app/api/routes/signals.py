from fastapi import APIRouter, Request
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.signal_snapshot import SignalSnapshot

router = APIRouter()


def serialize_signal_list_item(record: SignalSnapshot) -> dict:
    return {
        "signal_id": record.signal_id,
        "primary_ticker": record.primary_ticker,
        "decision": record.decision,
        "reason_code": record.reason_code,
        "decision_hint": record.decision_hint,
        "generated_at": record.generated_at.isoformat().replace("+00:00", "Z"),
    }


@router.get("/signals/latest")
def get_latest_signals(request: Request) -> dict:
    with SessionLocal() as session:
        records = session.scalars(
            select(SignalSnapshot)
            .order_by(desc(SignalSnapshot.generated_at))
            .limit(50)
        ).all()

    return {
        "data": [serialize_signal_list_item(record) for record in records],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": 50,
            "sort": "generated_at",
            "order": "desc",
        },
        "meta": request.state.meta,
    }
