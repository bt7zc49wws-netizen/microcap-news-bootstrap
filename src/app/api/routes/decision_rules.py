from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from app.decisioning.rules import DECISION_RULES_REGISTRY

router = APIRouter()

ALLOWED_DECISIONS = {"actionable", "watchlist", "no_trade"}
ALLOWED_REASON_CODES = {
    "WATCHLIST_ESCALATED_TO_ACTIONABLE",
    "SIGNAL_WATCHLIST",
    "SIGNAL_NO_TRADE",
}


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


def serialize_rule(rule: dict) -> dict:
    return {
        "rule_id": rule["rule_id"],
        "evaluation_order": rule["evaluation_order"],
        "decision": rule["decision"],
        "reason_code": rule["reason_code"],
        "reason_label": rule["reason_label"],
        "decision_summary": rule["decision_summary"],
    }


@router.get("/decision-rules")
def get_decision_rules(
    request: Request,
    decision: str | None = Query(default=None),
    reason_code: str | None = Query(default=None),
):
    if decision and decision not in ALLOWED_DECISIONS:
        return error_response(
            request,
            "invalid_parameter",
            "decision must be actionable, watchlist, or no_trade.",
            400,
        )

    if reason_code and reason_code not in ALLOWED_REASON_CODES:
        return error_response(
            request,
            "invalid_parameter",
            "reason_code is not supported.",
            400,
        )

    rules = list(DECISION_RULES_REGISTRY.values())

    if decision:
        rules = [rule for rule in rules if rule["decision"] == decision]

    if reason_code:
        rules = [rule for rule in rules if rule["reason_code"] == reason_code]

    rules = sorted(rules, key=lambda r: r["evaluation_order"])

    return {
        "data": [serialize_rule(rule) for rule in rules],
        "meta": request.state.meta,
    }


@router.get("/decision-rules/{rule_id}")
def get_decision_rule_detail(request: Request, rule_id: str):
    rule = DECISION_RULES_REGISTRY.get(rule_id)

    if rule is None:
        return error_response(
            request,
            "resource_not_found",
            "Requested decision rule was not found.",
            404,
        )

    return {
        "data": serialize_rule(rule),
        "meta": request.state.meta,
    }
