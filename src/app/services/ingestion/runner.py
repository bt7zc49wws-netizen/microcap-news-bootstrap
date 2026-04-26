from __future__ import annotations

import hashlib
import json
from typing import Any

from app.services.ingestion.adapters.press_release_feed import extract_items, fetch_feed
from app.services.ingestion.config import IngestionConfig
from app.services.ingestion.service import process_items
from app.db import SessionLocal
from app.models.ingestion_record import IngestionRecord
from app.services.ingestion.types import CanonicalIngestionRecord, FetchRun, RawSourceRecord


def run_live_ingestion(
    config: IngestionConfig,
    *,
    http_client: Any | None = None,
    persist: bool = True,
) -> tuple[FetchRun, list[RawSourceRecord], list[CanonicalIngestionRecord]]:
    if not config.live_source_enabled:
        raise ValueError("Live source ingestion is disabled.")
    if not config.live_source_url.strip():
        raise ValueError("LIVE_SOURCE_URL must be set when live ingestion is enabled.")

    feed_text = fetch_feed(
        config.live_source_url,
        timeout=config.live_source_timeout_seconds,
        http_client=http_client,
    )
    items = extract_items(feed_text)[: config.live_source_max_items_per_run]
    fetch_run, raw_records, records = process_items(
        items,
        source_name="live_press_release_feed",
    )
    if persist:
        persist_ingestion_records(records)
    return fetch_run, raw_records, records

def persist_ingestion_records(records):
    with SessionLocal() as session:
        for record in records:
            if record.validation_status == "rejected":
                continue
            external_id = hashlib.sha256(record.source_record_id.encode()).hexdigest()
            exists = session.query(IngestionRecord).filter_by(external_id=external_id).first()
            if exists:
                continue
            session.add(
                IngestionRecord(
                    record_id=record.record_id,
                    external_id=external_id,
                    source_name=record.source_name,
                    source_type="live",
                    symbol=record.primary_ticker or "UNKNOWN",
                    headline=record.title,
                    source_event_time=record.published_at or record.ingested_at,
                    published_at=record.published_at or record.ingested_at,
                    ingested_at=record.ingested_at,
                    processed_at=record.processed_at,
                    status=str(record.validation_status),
                    quality_flags=json.dumps([str(flag) for flag in record.quality_flags]),
                    is_duplicate=record.is_duplicate,
                )
            )
        session.commit()
