from app.db import Base, engine


def init_db():
    # IMPORTANT: force model registration
    import app.models.jobs  # noqa
    import app.models.ingestion_record  # noqa
    import app.models.decision_snapshot  # noqa

    Base.metadata.create_all(bind=engine)
