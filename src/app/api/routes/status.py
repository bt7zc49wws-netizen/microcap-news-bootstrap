from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def status():
    now = datetime.now(timezone.utc).isoformat()

    return {
        "data": {
            "overall_status": "ok",
            "is_stale": False,
            "freshness_threshold_seconds": 60,
            "last_data_update_at": now,
            "last_signal_generated_at": now,
            "freshness_evaluated_at": now,
            "dependencies": {
                "read_model": "ok"
            }
        },
        "meta": {
            "api_version": "v1",
            "request_id": str(uuid4()),
            "timestamp": now
        }
    }
