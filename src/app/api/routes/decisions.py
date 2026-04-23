import re
import uuid

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import asc, desc, select

from app.db import SessionLocal
from app.models.decision_snapshot import DecisionSnapshot

router = APIRouter()

ALLOWED_DECISIONS = {"actionable", "watchlist", "no_trade"}
ALLOWED_SORTS = {"generated_at"}
ALLOWED_ORDERS = {"asc", "desc"}
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


def serialize_decision_list_item(record: DecisionSnapshot) -> dict:
    return {
        "decision_id": record.decision_id,
        "primary_ticker": record.primary_ticker,
        "decision": record.decision,
        "reason_code": record.reason_code,
        "generated_at": record.generated_at.isoformat().replace("+00:00", "Z"),
    }


def serialize_decision_detail(record: DecisionSnapshot) -> dict:
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
def get_latest_decisions(
    request: Request,
    decision: str | None = Query(default=None),
    primary_ticker: str | None = Query(default=None),
    limit: int = Query(default=50),
    sort: str = Query(default="generated_at"),
    order: str = Query(default="desc"),
):
    if decision and decision not in ALLOWED_DECISIONS:
        return error_response(
            request,
            "invalid_parameter",
            "decision must be actionable, watchlist, or no_trade.",
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
            "Only generated_at sort is supported.",
            400,
        )

    if order not in ALLOWED_ORDERS:
        return error_response(
            request,
            "invalid_parameter",
            "Order must be asc or desc.",
            400,
        )

    query = select(DecisionSnapshot)

    if decision:
        query = query.where(DecisionSnapshot.decision == decision)

    if normalized_ticker:
        query = query.where(DecisionSnapshot.primary_ticker == normalized_ticker)

    sort_column = DecisionSnapshot.generated_at
    ordering = desc(sort_column) if order == "desc" else asc(sort_column)

    query = query.order_by(ordering).limit(limit)

    with SessionLocal() as session:
        records = session.scalars(query).all()

    return {
        "data": [serialize_decision_list_item(record) for record in records],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": limit,
            "sort": sort,
            "order": order,
        },
        "meta": request.state.meta,
    }


@router.get("/decisions/{decision_id}")
def get_decision_detail(request: Request, decision_id: str):
    try:
        uuid.UUID(decision_id)
    except ValueError:
        return error_response(
            request,
            "invalid_parameter",
            "decision_id must be a valid UUID.",
            400,
        )

    with SessionLocal() as session:
        record = session.get(DecisionSnapshot, decision_id)

    if record is None:
        return error_response(
            request,
            "resource_not_found",
            "Requested decision was not found.",
            404,
        )

    return {
        "data": serialize_decision_detail(record),
        "meta": request.state.meta,
    }
