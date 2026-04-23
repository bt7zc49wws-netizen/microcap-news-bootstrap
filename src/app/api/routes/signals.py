from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import desc, select

from app.db import SessionLocal
from app.models.signal_snapshot import SignalSnapshot

router = APIRouter()

ALLOWED_DECISIONS = {"watchlist", "no_trade"}


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
):
    if decision and decision not in ALLOWED_DECISIONS:
        return error_response(
            request,
            "invalid_parameter",
            "decision must be watchlist or no_trade.",
            400,
        )

    query = select(SignalSnapshot)

    if decision:
        query = query.where(SignalSnapshot.decision == decision)

    query = query.order_by(desc(SignalSnapshot.generated_at)).limit(50)

    with SessionLocal() as session:
        records = session.scalars(query).all()

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
