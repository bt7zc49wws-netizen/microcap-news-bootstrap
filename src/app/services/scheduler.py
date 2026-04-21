import logging
import time

from app.config import settings
from app.db import SessionLocal, wait_for_db_and_tables
from app.models.job import Job


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("scheduler")


def run() -> None:
    logger.info("scheduler waiting for db/tables")
    wait_for_db_and_tables(["jobs"])
    logger.info("scheduler started")

    while True:
        try:
            with SessionLocal() as session:
                tick_job = Job(job_type="scheduler_tick", payload='{"source":"scheduler"}')
                ingest_job = Job(job_type="ingest_news", payload='{"source":"scheduler"}')
                session.add(tick_job)
                session.add(ingest_job)
                session.commit()
                logger.info("scheduled job type=%s id=%s", tick_job.job_type, tick_job.job_id)
                logger.info("scheduled job type=%s id=%s", ingest_job.job_type, ingest_job.job_id)
        except Exception as exc:
            logger.exception("scheduler loop error: %s", exc)

        time.sleep(settings.SCHEDULER_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
