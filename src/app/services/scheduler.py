import logging
import time

from app.config import settings
from app.db import SessionLocal, init_db
from app.models.job import Job


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("scheduler")


def run() -> None:
    init_db()
    logger.info("scheduler started")

    while True:
        try:
            with SessionLocal() as session:
                job = Job(job_type="scheduler_tick", payload='{"source":"scheduler"}')
                session.add(job)
                session.commit()
                logger.info("scheduled job type=%s id=%s", job.job_type, job.job_id)
        except Exception as exc:
            logger.exception("scheduler loop error: %s", exc)

        time.sleep(settings.SCHEDULER_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
