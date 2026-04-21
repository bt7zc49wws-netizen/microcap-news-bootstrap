import logging
import time
from datetime import datetime, timezone

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal, init_db
from app.models.ingestion_record import IngestionRecord
from app.models.job import Job
from app.providers.mock_news_provider import fetch_mock_news


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("worker")


def process_ingest_news() -> None:
    records = fetch_mock_news()

    with SessionLocal() as session:
        for record in records:
            item = IngestionRecord(
                source_name=record["source_name"],
                source_type=record["source_type"],
                symbol=record["symbol"],
                headline=record["headline"],
                published_at=record["published_at"],
                status="INGESTED",
            )
            session.add(item)
        session.commit()


def process_job(job: Job) -> None:
    if job.job_type == "scheduler_tick":
        job.result = '{"message":"tick-ok"}'
        job.status = "SUCCESS"

    elif job.job_type == "ingest_news":
        process_ingest_news()
        job.result = '{"message":"ingestion-ok"}'
        job.status = "SUCCESS"

    elif job.job_type == "smoke":
        job.result = '{"message":"smoke-ok"}'
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
                logger.info(
                    "completed job id=%s type=%s status=%s",
                    job.job_id,
                    job.job_type,
                    job.status,
                )

        except Exception as exc:
            logger.exception("worker loop error: %s", exc)
            time.sleep(settings.WORKER_POLL_SECONDS)


if __name__ == "__main__":
    run()
