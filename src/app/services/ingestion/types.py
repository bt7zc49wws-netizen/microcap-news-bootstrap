from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class ValidationStatus(str, Enum):
    ACCEPTED = "accepted"
    ACCEPTED_WITH_FLAGS = "accepted_with_flags"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class QualityFlag(str, Enum):
    PARTIAL_PARSE = "PARTIAL_PARSE"
    TICKER_MISSING = "TICKER_MISSING"
    BODY_FROM_DESCRIPTION = "BODY_FROM_DESCRIPTION"
    STALE_RECORD = "STALE_RECORD"


@dataclass
class FetchRun:
    fetch_run_id: str
    source_name: str
    run_started_at: datetime
    run_finished_at: Optional[datetime] = None
    run_status: str = "started"
    error_summary: Optional[str] = None
    records_fetched: int = 0
    records_accepted: int = 0
    records_duplicated: int = 0
    records_quarantined: int = 0
    records_rejected: int = 0


@dataclass
class RawSourceRecord:
    raw_record_id: str
    source_name: str
    source_record_id: str
    fetch_run_id: str
    fetched_at: datetime
    source_url: Optional[str]
    raw_payload: dict
    content_hash: str
    adapter_version: str
    title: Optional[str] = None
    body: Optional[str] = None


@dataclass
class CanonicalIngestionRecord:
    record_id: str
    source_name: str
    source_record_id: str
    source_url: Optional[str]
    title: str
    body_text: str
    published_at: Optional[datetime]
    ingested_at: datetime
    processed_at: datetime
    primary_ticker: Optional[str]
    company_name: Optional[str]
    language: str
    content_hash: str
    dedupe_key: str
    is_duplicate: bool
    is_stale: bool
    validation_status: ValidationStatus
    quality_flags: List[QualityFlag] = field(default_factory=list)
    raw_record_ref: Optional[str] = None
    normalization_version: str = "canonical_ingest_v1"
