from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from uuid import uuid4
from typing import Any

from app.services.ingestion.types import CanonicalIngestionRecord, QualityFlag, ValidationStatus

SOURCE_NAME = "finnhub_news"
ADAPTER_VERSION = "finnhub_news_adapter_v1"
NORMALIZATION_VERSION = "canonical_ingest_v1"


def compute_content_hash(title: str, body_text: str) -> str:
    payload = f"{title.strip()}\n{body_text.strip()}".encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def normalize_finnhub_news_item(
    item: dict[str, Any],
    *,
    ingested_at: datetime | None = None,
) -> CanonicalIngestionRecord:
    ingested_at = ingested_at or datetime.now(UTC)
    processed_at = ingested_at

    source_record_id = str(item.get("id") or item.get("url") or uuid4())
    title = str(item.get("headline") or "").strip()
    body_text = str(item.get("summary") or "").strip()
    source_url = item.get("url")
    primary_ticker = item.get("related")
    published_at = datetime.fromtimestamp(item["datetime"], UTC) if item.get("datetime") else None

    quality_flags: list[QualityFlag] = []
    if not primary_ticker:
        quality_flags.append(QualityFlag.TICKER_MISSING)

    validation_status = ValidationStatus.ACCEPTED_WITH_FLAGS if quality_flags else ValidationStatus.ACCEPTED
    content_hash = compute_content_hash(title=title, body_text=body_text)

    return CanonicalIngestionRecord(
        record_id=str(uuid4()),
        source_name=SOURCE_NAME,
        source_record_id=source_record_id,
        source_url=source_url,
        title=title,
        body_text=body_text,
        published_at=published_at,
        ingested_at=ingested_at,
        processed_at=processed_at,
        primary_ticker=primary_ticker,
        company_name=None,
        language="en",
        content_hash=content_hash,
        dedupe_key=f"{SOURCE_NAME}:{source_record_id}",
        is_duplicate=False,
        is_stale=False,
        validation_status=validation_status,
        quality_flags=quality_flags,
        raw_record_ref=None,
        normalization_version=NORMALIZATION_VERSION,
    )
