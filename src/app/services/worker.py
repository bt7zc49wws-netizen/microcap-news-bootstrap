import logging
import time
from datetime import datetime, timezone

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal, wait_for_db_and_tables
from app.models.event_candidate import EventCandidate
from app.models.ingestion_record import IngestionRecord
from app.models.job import Job
from app.providers.mock_news_provider import fetch_mock_news


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("worker")


def process_ingest_news() -> None:
    records = fetch_mock_news()

    with SessionLocal() as session:
        for record in records:
            existing = session.scalars(
                select(IngestionRecord).where(IngestionRecord.external_id == record["external_id"])
            ).first()

            if existing is not None:
                logger.info("duplicate ingestion skipped external_id=%s", record["external_id"])
                continue

            item = IngestionRecord(
                external_id=record["external_id"],
                source_name=record["source_name"],
                source_type=record["source_type"],
                symbol=record["symbol"],
                headline=record["headline"],
                source_event_time=record["source_event_time"],
                published_at=record["published_at"],
                status="INGESTED",
                quality_flags=record["quality_flags"],
                is_duplicate=False,
                processed_at=datetime.now(timezone.utc),
            )
            session.add(item)

        session.commit()


def classify_record(record: IngestionRecord) -> dict:
    headline_lower = record.headline.lower()

    if "financing" in headline_lower:
        return {
            "event_family": "financing",
            "event_type": "financing_news",
            "classification_status": "EVENT_CANDIDATE",
            "reason_code": "FINANCING_KEYWORD_MATCH",
            "noise_flags": "[]",
        }

    if "offering" in headline_lower:
        return {
            "event_family": "financing",
            "event_type": "offering_news",
            "classification_status": "EVENT_CANDIDATE",
            "reason_code": "OFFERING_KEYWORD_MATCH",
            "noise_flags": "[]",
        }

    return {
        "event_family": "other",
        "event_type": "uncategorized",
        "classification_status": "LOW_PRIORITY_CANDIDATE",
        "reason_code": "NO_CLEAR_EVENT_MATCH",
        "noise_flags": '["low_signal"]',
    }


def process_classify_news() -> None:
    with SessionLocal() as session:
        records = session.scalars(
            select(IngestionRecord).order_by(IngestionRecord.published_at)
        ).all()

        for record in records:
            existing = session.scalars(
                select(EventCandidate).where(EventCandidate.source_record_id == record.record_id)
            ).first()

            if existing is not None:
                logger.info("duplicate classification skipped source_record_id=%s", record.record_id)
                continue

            result = classify_record(record)

            candidate = EventCandidate(
                source_record_id=record.record_id,
                source_name=record.source_name,
                primary_ticker=record.symbol,
                event_family=result["event_family"],
                event_type=result["event_type"],
                classification_status=result["classification_status"],
                reason_code=result["reason_code"],
                noise_flags=result["noise_flags"],
                headline=record.headline,
            )
            session.add(candidate)

        session.commit()


def process_job(job: Job) -> None:
    if job.job_type == "scheduler_tick":
        job.result = '{"message":"tick-ok"}'
        job.status = "SUCCESS"

    elif job.job_type == "ingest_news":
        process_ingest_news()
        job.result = '{"message":"ingestion-ok"}'
        job.status = "SUCCESS"

    elif job.job_type == "classify_news":
        process_classify_news()
        job.result = '{"message":"classification-ok"}'
        job.status = "SUCCESS"

    elif job.job_type == "smoke":
        job.result = '{"message":"smoke-ok"}'
        job.status = "SUCCESS"

    else:
        job.result = '{"message":"skipped"}'
        job.status = "SKIPPED"

    job.finished_at = datetime.now(timezone.utc)


def run() -> None:
    logger.info("worker waiting for db/tables")
    wait_for_db_and_tables(["jobs", "ingestion_records", "event_candidates"])
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
