import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class IngestionRecord(Base):
    __tablename__ = "ingestion_records"

    record_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    external_id: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    source_name: Mapped[str] = mapped_column(String(64), index=True)
    source_type: Mapped[str] = mapped_column(String(32), default="mock")
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    headline: Mapped[str] = mapped_column(Text)
    source_event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="INGESTED")
    quality_flags: Mapped[str] = mapped_column(Text, default="[]")
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
