from fastapi import APIRouter, Request
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.signal_snapshot import SignalSnapshot

router = APIRouter()


@router.get("/signals/latest")
def get_latest_signals(request: Request) -> dict:
    with SessionLocal() as session:
        records = session.scalars(
            select(SignalSnapshot)
            .order_by(desc(SignalSnapshot.generated_at))
            .limit(50)
        ).all()

    return {
        "data": [
            {
                "signal_id": record.signal_id,
                "source_candidate_id": record.source_candidate_id,
                "primary_ticker": record.primary_ticker,
                "decision": record.decision,
                "reason_code": record.reason_code,
                "reason_label": record.reason_label,
                "decision_hint": record.decision_hint,
                "generated_at": record.generated_at.isoformat().replace("+00:00", "Z"),
            }
            for record in records
        ],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": 50,
            "sort": "generated_at",
            "order": "desc",
        },
        "meta": request.state.meta,
    }
