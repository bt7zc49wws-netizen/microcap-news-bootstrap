import re

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import asc, desc, select

from app.db import SessionLocal
from app.models.signal_snapshot import SignalSnapshot

router = APIRouter()

ALLOWED_DECISIONS = {"watchlist", "no_trade"}
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
def get_latest_signals(
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
            "decision must be watchlist or no_trade.",
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

    query = select(SignalSnapshot)

    if decision:
        query = query.where(SignalSnapshot.decision == decision)

    if normalized_ticker:
        query = query.where(SignalSnapshot.primary_ticker == normalized_ticker)

    sort_column = SignalSnapshot.generated_at
    ordering = desc(sort_column) if order == "desc" else asc(sort_column)

    query = query.order_by(ordering).limit(limit)

    with SessionLocal() as session:
        records = session.scalars(query).all()

    return {
        "data": [serialize_signal_list_item(record) for record in records],
        "pagination": {
            "next_cursor": "",
            "has_more": False,
            "limit": limit,
            "sort": sort,
            "order": order,
        },
        "meta": request.state.meta,
    }
