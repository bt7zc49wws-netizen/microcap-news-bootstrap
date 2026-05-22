from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class DecisionSnapshot(Base):
    __tablename__ = "decision_snapshots"

    decision_id: Mapped[str] = mapped_column(String, primary_key=True)
    generated_at: Mapped[str] = mapped_column(String, index=True)

    symbol: Mapped[str] = mapped_column(String, default="")
    decision: Mapped[str] = mapped_column(String, default="neutral")
