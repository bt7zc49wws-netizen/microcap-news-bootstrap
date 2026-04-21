from datetime import datetime, timezone

from fastapi import APIRouter, Request
from sqlalchemy import desc, select

from app.config import settings
from app.db import SessionLocal, ping_db
from app.models.job import Job

router = APIRouter()


@router.get("/status")
def status(request: Request) -> dict:
    db_ok = ping_db()

    last_successful_run = None
    with SessionLocal() as session:
        job = session.scalars(
            select(Job)
            .where(Job.status == "SUCCESS")
            .order_by(desc(Job.finished_at))
            .limit(1)
        ).first()
        if job and job.finished_at:
            last_successful_run = job.finished_at

    now = datetime.now(timezone.utc)
    is_stale = True
    if last_successful_run is not None:
        age = (now - last_successful_run).total_seconds()
        is_stale = age > settings.FRESHNESS_THRESHOLD_SECONDS

    overall_status = "degraded"
    if db_ok and not is_stale and last_successful_run is not None:
        overall_status = "ok"

    ts = last_successful_run.isoformat().replace("+00:00", "Z") if last_successful_run else now.isoformat().replace("+00:00", "Z")

    return {
        "data": {
            "overall_status": overall_status,
            "last_data_update_at": ts,
            "last_signal_generated_at": ts,
            "is_stale": is_stale,
            "freshness_evaluated_at": now.isoformat().replace("+00:00", "Z"),
            "freshness_threshold_seconds": settings.FRESHNESS_THRESHOLD_SECONDS,
            "dependencies": {
                "read_model": "ok" if db_ok else "unavailable",
            },
        },
        "meta": request.state.meta,
    }
