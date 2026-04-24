from __future__ import annotations

from typing import Any

from app.services.ingestion.adapters.press_release_feed import extract_items, fetch_feed
from app.services.ingestion.config import IngestionConfig
from app.services.ingestion.service import process_items
from app.services.ingestion.types import CanonicalIngestionRecord, FetchRun, RawSourceRecord


def run_live_ingestion(
    config: IngestionConfig,
    *,
    http_client: Any | None = None,
) -> tuple[FetchRun, list[RawSourceRecord], list[CanonicalIngestionRecord]]:
    if not config.live_source_enabled:
        raise ValueError("Live source ingestion is disabled.")

    if not config.live_source_url.strip():
        raise ValueError("LIVE_SOURCE_URL must be set when live ingestion is enabled.")

    xml_text = fetch_feed(
        config.live_source_url,
        http_client=http_client,
        timeout=config.live_source_timeout_seconds,
    )
    items = extract_items(xml_text)

    if config.live_source_max_items_per_run > 0:
        items = items[: config.live_source_max_items_per_run]

    return process_items(items)
