from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class ValidationStatus(StrEnum):
    ACCEPTED = "accepted"
    ACCEPTED_WITH_FLAGS = "accepted_with_flags"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"


class QualityFlag(StrEnum):
    TICKER_MISSING = "ticker_missing"
    TICKER_HEURISTIC = "ticker_heuristic"
    COMPANY_NAME_HEURISTIC = "company_name_heuristic"
    SOURCE_RECORD_ID_FALLBACK = "source_record_id_fallback"
    BODY_FROM_DESCRIPTION = "body_from_description"
    PUBLISHED_AT_FALLBACK = "published_at_fallback"
    POSSIBLE_NEAR_DUPLICATE = "possible_near_duplicate"
    STALE_RECORD = "stale_record"
    HTML_HEAVY_CONTENT = "html_heavy_content"
    PARTIAL_PARSE = "partial_parse"


@dataclass(slots=True)
class FetchRun:
    fetch_run_id: str
    source_name: str
    run_started_at: datetime
    run_finished_at: datetime | None = None
    run_status: str = "started"
    records_fetched: int = 0
    records_accepted: int = 0
    records_rejected: int = 0
    records_quarantined: int = 0
    records_duplicated: int = 0
    error_summary: str | None = None


@dataclass(slots=True)
class RawSourceRecord:
    raw_record_id: str
    source_name: str
    source_record_id: str
    fetch_run_id: str
    fetched_at: datetime
    source_url: str | None
    raw_payload: dict[str, Any]
    content_hash: str
    adapter_version: str


@dataclass(slots=True)
class CanonicalIngestionRecord:
    record_id: str
    source_name: str
    source_record_id: str
    source_url: str | None
    title: str
    body_text: str
    published_at: datetime | None
    ingested_at: datetime
    processed_at: datetime
    primary_ticker: str | None
    company_name: str | None
    language: str | None
    content_hash: str
    dedupe_key: str
    is_duplicate: bool
    is_stale: bool
    validation_status: ValidationStatus
    quality_flags: list[QualityFlag] = field(default_factory=list)
    raw_record_ref: str | None = None
    normalization_version: str = "canonical_ingest_v1"
