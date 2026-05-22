
from sqlalchemy import Column, String
from app.db_models.db import Base

class DecisionSnapshotDB(Base):
    __tablename__ = "decision_snapshots"

    id = Column(String, primary_key=True)
    decision = Column(String)
