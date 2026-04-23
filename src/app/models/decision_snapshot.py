import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DecisionSnapshot(Base):
    __tablename__ = "decision_snapshots"

    decision_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    source_signal_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    primary_ticker: Mapped[str] = mapped_column(String(16), index=True)
    decision: Mapped[str] = mapped_column(String(32), index=True)
    reason_code: Mapped[str] = mapped_column(String(64))
    reason_label: Mapped[str] = mapped_column(String(128), default="Unspecified")
    decision_summary: Mapped[str] = mapped_column(Text, default="")
    decision_context: Mapped[str] = mapped_column(Text, default="{}")
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
