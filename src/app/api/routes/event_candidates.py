from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import asc, desc, select

from app.db import SessionLocal
from app.models.event_candidate import EventCandidate

router = APIRouter()

ALLOWED_SORTS = {"classified_at"}
ALLOWED_ORDERS = {"asc", "desc"}


def error_response(request: Request, error_code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "error_code": error_code,
                "message": message,
            },
            "meta": request.state.meta,
        },
    )


@router.get("/event-candidates/latest")
def get_latest_event_candidates(
    request: Request,
    classification_status: str | None = Query(default=None),
    primary_ticker: str | None = Query(default=None),
    limit: int = Query(default=50),
    sort: str = Query(default="classified_at"),
    order: str = Query(default="desc"),
):
    if limit < 1 or limit > 100:
        return error_response(
            request,
            "limit_out_of_range",
            "Limit must be between 1 and 100.",
            400,
        )

    if sort not in ALLOWED_SORTS:
        return error_response(
            request,
            "unsupported_sort",
            "Only classified_at sort is supported.",
            400,
        )

    if order not in ALLOWED_ORDERS:
        return error_response(
            request,
            "invalid_parameter",
            "Order must be asc or desc.",
            400,
        )

    query = select(EventCandidate)

    if classification_status:
        query = query.where(EventCandidate.classification_status == classification_status)

    if primary_ticker:
        query = query.where(EventCandidate.primary_ticker == primary_ticker.upper())

    sort_column = EventCandidate.classified_at
    ordering = desc(sort_column) if order == "desc" else asc(sort_column)

    query = query.order_by(ordering).limit(limit)

    with SessionLocal() as session:
        records = session.scalars(query).all()

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
            "limit": limit,
            "sort": sort,
            "order": order,
        },
        "meta": request.state.meta,
    }
