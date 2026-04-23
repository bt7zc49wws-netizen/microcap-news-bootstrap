from fastapi import APIRouter, Request

from app.decisioning.rules import DECISION_RULES_REGISTRY

router = APIRouter()


@router.get("/decision-rules")
def get_decision_rules(request: Request) -> dict:
    rules = list(DECISION_RULES_REGISTRY.values())

    return {
        "data": [
            {
                "rule_id": rule["rule_id"],
                "decision": rule["decision"],
                "reason_code": rule["reason_code"],
                "reason_label": rule["reason_label"],
                "decision_summary": rule["decision_summary"],
            }
            for rule in rules
        ],
        "meta": request.state.meta,
    }
