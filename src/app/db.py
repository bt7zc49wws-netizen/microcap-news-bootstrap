import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    import app.models.job  # noqa: F401
    import app.models.ingestion_record  # noqa: F401
    import app.models.event_candidate  # noqa: F401
    import app.models.signal_snapshot  # noqa: F401
    Base.metadata.create_all(bind=engine)


def ping_db() -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def table_exists(table_name: str) -> bool:
    query = text(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = :table_name
        )
        """
    )
    with engine.connect() as conn:
        return bool(conn.execute(query, {"table_name": table_name}).scalar())


def wait_for_db_and_tables(
    required_tables: list[str],
    max_attempts: int = 60,
    sleep_seconds: int = 2,
) -> None:
    for _ in range(max_attempts):
        try:
            if not ping_db():
                raise RuntimeError("database ping failed")

            missing_tables = [t for t in required_tables if not table_exists(t)]
            if not missing_tables:
                return

        except SQLAlchemyError:
            pass

        time.sleep(sleep_seconds)

    raise RuntimeError(
        f"database/tables not ready after wait; required_tables={required_tables}"
    )
