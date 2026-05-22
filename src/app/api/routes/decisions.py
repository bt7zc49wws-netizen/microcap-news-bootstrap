from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

router = APIRouter()


@router.get("/decisions/latest")
def get_latest_decisions(limit: int = 50):
    decisions = [
        {
            "primary_ticker": "ABCD",
            "decision": "actionable",
            "rule_id": "abcd_actionable_seed",
            "rule_version": "decision_rules_v1",
        },
        {
            "primary_ticker": "WXYZ",
            "decision": "watchlist",
            "rule_id": "watchlist_passthrough",
            "rule_version": "decision_rules_v1",
        },
        {
            "primary_ticker": "ZZZZ",
            "decision": "no_trade",
            "rule_id": "no_trade_passthrough",
            "rule_version": "decision_rules_v1",
        },
    ]

    return {
        "data": decisions[:limit],
        "meta": {
            "count": min(len(decisions), limit),
            "has_more": len(decisions) > limit,
            "request_id": str(uuid4()),
            "api_version": "v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
