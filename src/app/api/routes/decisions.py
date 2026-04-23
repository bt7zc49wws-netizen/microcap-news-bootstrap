import re

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.decision_snapshot import DecisionSnapshot

router = APIRouter()

ALLOWED_DECISIONS = {"actionable", "watchlist", "no_trade"}
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


@router.get("/decisions/latest")
def get_latest_decisions(
    request: Request,
    decision: str | None = Query(default=None),
    primary_ticker: str | None = Query(default=None),
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

    query = select(DecisionSnapshot)

    if decision:
        query = query.where(DecisionSnapshot.decision == decision)

    if normalized_ticker:
        query = query.where(DecisionSnapshot.primary_ticker == normalized_ticker)

    query = query.order_by(desc(DecisionSnapshot.generated_at)).limit(50)

    with SessionLocal() as session:
        records = session.scalars(query).all()

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
