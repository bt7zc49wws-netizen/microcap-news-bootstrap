from datetime import datetime
import re

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import and_, asc, desc, or_, select

from app.db import SessionLocal
from app.models.event_candidate import EventCandidate

router = APIRouter()

ALLOWED_SORTS = {"classified_at"}
ALLOWED_ORDERS = {"asc", "desc"}
ALLOWED_CLASSIFICATION_STATUSES = {"EVENT_CANDIDATE", "LOW_PRIORITY_CANDIDATE"}
TICKER_PATTERN = re.compile(r"^[A-Z][A-Z\.]{0,9}$")


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


def serialize_candidate_list_item(record: EventCandidate) -> dict:
    return {
        "candidate_id": record.candidate_id,
        "primary_ticker": record.primary_ticker,
        "event_family": record.event_family,
        "event_type": record.event_type,
        "classification_status": record.classification_status,
        "reason_code": record.reason_code,
        "candidate_priority": record.candidate_priority,
        "decision_hint": record.decision_hint,
        "classified_at": record.classified_at.isoformat().replace("+00:00", "Z"),
    }


def serialize_candidate_detail(record: EventCandidate) -> dict:
    return {
        "candidate_id": record.candidate_id,
        "source_record_id": record.source_record_id,
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


def encode_cursor(classified_at: datetime, candidate_id: str) -> str:
    return f"{classified_at.isoformat()}|{candidate_id}"


def decode_cursor(cursor: str) -> tuple[datetime, str]:
    try:
        ts_str, candidate_id = cursor.split("|", 1)
        ts = datetime.fromisoformat(ts_str)
        return ts, candidate_id
    except Exception as exc:
        raise ValueError("invalid cursor") from exc


@router.get("/event-candidates/latest")
def get_latest_event_candidates(
    request: Request,
    classification_status: str | None = Query(default=None),
    primary_ticker: str | None = Query(default=None),
    limit: int = Query(default=50),
    sort: str = Query(default="classified_at"),
    order: str = Query(default="desc"),
    cursor: str | None = Query(default=None),
):
    if classification_status and classification_status not in ALLOWED_CLASSIFICATION_STATUSES:
        return error_response(
            request,
            "invalid_parameter",
            "classification_status must be EVENT_CANDIDATE or LOW_PRIORITY_CANDIDATE.",
            400,
        )

    if primary_ticker:
        normalized_ticker = primary_ticker.upper()
        if not TICKER_PATTERN.fullmatch(normalized_ticker):
            return error_response(
                request,
                "invalid_parameter",
                "primary_ticker must match the allowed ticker format.",
                400,
            )
    else:
        normalized_ticker = None

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

    if normalized_ticker:
        query = query.where(EventCandidate.primary_ticker == normalized_ticker)

    if cursor:
        try:
            cursor_ts, cursor_candidate_id = decode_cursor(cursor)
        except ValueError:
            return error_response(
                request,
                "invalid_cursor",
                "Cursor could not be parsed.",
                400,
            )

        if order == "desc":
            query = query.where(
                or_(
                    EventCandidate.classified_at < cursor_ts,
                    and_(
                        EventCandidate.classified_at == cursor_ts,
                        EventCandidate.candidate_id < cursor_candidate_id,
                    ),
                )
            )
        else:
            query = query.where(
                or_(
                    EventCandidate.classified_at > cursor_ts,
                    and_(
                        EventCandidate.classified_at == cursor_ts,
                        EventCandidate.candidate_id > cursor_candidate_id,
                    ),
                )
            )

    if order == "desc":
        query = query.order_by(
            desc(EventCandidate.classified_at),
            desc(EventCandidate.candidate_id),
        )
    else:
        query = query.order_by(
            asc(EventCandidate.classified_at),
            asc(EventCandidate.candidate_id),
        )

    query = query.limit(limit + 1)

    with SessionLocal() as session:
        records = session.scalars(query).all()

    has_more = len(records) > limit
    visible_records = records[:limit]

    next_cursor = ""
    if has_more and visible_records:
        last_record = visible_records[-1]
        next_cursor = encode_cursor(last_record.classified_at, last_record.candidate_id)

    return {
        "data": [serialize_candidate_list_item(record) for record in visible_records],
        "pagination": {
            "next_cursor": next_cursor,
            "has_more": has_more,
            "limit": limit,
            "sort": sort,
            "order": order,
        },
        "meta": request.state.meta,
    }


@router.get("/event-candidates/{candidate_id}")
def get_event_candidate_detail(request: Request, candidate_id: str):
    with SessionLocal() as session:
        record = session.get(EventCandidate, candidate_id)

    if record is None:
        return error_response(
            request,
            "resource_not_found",
            "Requested event candidate was not found.",
            404,
        )

    return {
        "data": serialize_candidate_detail(record),
        "meta": request.state.meta,
    }
