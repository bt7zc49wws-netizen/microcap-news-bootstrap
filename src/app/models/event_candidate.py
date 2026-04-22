import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class EventCandidate(Base):
    __tablename__ = "event_candidates"

    candidate_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    source_record_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    source_name: Mapped[str] = mapped_column(String(64), index=True)
    primary_ticker: Mapped[str] = mapped_column(String(16), index=True)
    event_family: Mapped[str] = mapped_column(String(64), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    classification_status: Mapped[str] = mapped_column(String(32), default="EVENT_CANDIDATE")
    reason_code: Mapped[str] = mapped_column(String(64), default="UNSPECIFIED")
    noise_flags: Mapped[str] = mapped_column(Text, default="[]")
    headline: Mapped[str] = mapped_column(Text)
    classified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
