from fastapi import APIRouter, Request
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.event_candidate import EventCandidate

router = APIRouter()


@router.get("/event-candidates/latest")
def get_latest_event_candidates(request: Request) -> dict:
    with SessionLocal() as session:
        records = session.scalars(
            select(EventCandidate)
            .order_by(desc(EventCandidate.classified_at))
            .limit(50)
        ).all()

    return {
        "data": [
            {
                "candidate_id": record.candidate_id,
                "source_external_id": record.source_external_id,
                "source_name": record.source_name,
                "primary_ticker": record.primary_ticker,
                "event_family": record.event_family,
                "event_type": record.event_type,
                "classification_status": record.classification_status,
                "reason_code": record.reason_code,
                "reason_label": record.reason_label,
                "candidate_priority": record.candidate_priority,
                "decision_hint": record.decision_hint,
                "explanation_summary": record.explanation_summary,
                "source_event_time": record.source_event_time.isoformat().replace("+00:00", "Z"),
                "source_published_at": record.source_published_at.isoformat().replace("+00:00", "Z"),
                "classified_at": record.classified_at.isoformat().replace("+00:00", "Z"),
            }
            for record in records
        ],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": 50,
            "sort": "classified_at",
            "order": "desc",
        },
        "meta": request.state.meta,
    }
