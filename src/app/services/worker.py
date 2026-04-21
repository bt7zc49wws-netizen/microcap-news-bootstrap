import logging
import time
from datetime import datetime, timezone

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal, init_db
from app.models.job import Job


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("worker")


def process_job(job: Job) -> None:
    if job.job_type in {"smoke", "scheduler_tick"}:
        job.result = '{"message":"ok"}'
        job.status = "SUCCESS"
    else:
        job.result = '{"message":"skipped"}'
        job.status = "SKIPPED"
    job.finished_at = datetime.now(timezone.utc)


def run() -> None:
    init_db()
    logger.info("worker started")

    while True:
        try:
            with SessionLocal() as session:
                job = session.scalars(
                    select(Job)
                    .where(Job.status == "PENDING")
                    .order_by(Job.triggered_at)
                    .limit(1)
                ).first()

                if job is None:
                    time.sleep(settings.WORKER_POLL_SECONDS)
                    continue

                job.status = "RUNNING"
                job.started_at = datetime.now(timezone.utc)
                session.commit()

                try:
                    process_job(job)
                except Exception as exc:
                    job.status = "FAILED"
                    job.result = f'{{"error":"{str(exc)}"}}'
                    job.finished_at = datetime.now(timezone.utc)

                session.commit()
                logger.info("completed job id=%s type=%s status=%s", job.job_id, job.job_type, job.status)

        except Exception as exc:
            logger.exception("worker loop error: %s", exc)
            time.sleep(settings.WORKER_POLL_SECONDS)


if __name__ == "__main__":
    run()
