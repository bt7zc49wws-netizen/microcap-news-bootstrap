
from sqlalchemy import Column, String
from app.db_models.db import Base

class IngestionRecordDB(Base):
    __tablename__ = "ingestion_records"

    external_id = Column(String, primary_key=True)
    source_name = Column(String)
