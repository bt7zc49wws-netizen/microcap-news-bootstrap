from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.ingestion.adapters.press_release_feed import (
    build_raw_record,
    normalize_item,
)
from app.services.ingestion.dedupe import compute_dedupe_key, is_exact_duplicate
from app.services.ingestion.types import (
    CanonicalIngestionRecord,
    FetchRun,
    RawSourceRecord,
)
from app.services.ingestion.validation import validate_record


def process_items(
    items: list[dict[str, Any]],
    *,
    source_name: str = "press_release_feed_v1",
    fetch_run_id: str = "run-1",
    fetched_at: datetime | None = None,
    seen_source_keys: set[str] | None = None,
    seen_content_hashes: set[str] | None = None,
) -> tuple[FetchRun, list[RawSourceRecord], list[CanonicalIngestionRecord]]:
    fetched_at = fetched_at or datetime.now(timezone.utc)
    seen_source_keys = seen_source_keys or set()
    seen_content_hashes = seen_content_hashes or set()

    run = FetchRun(
        fetch_run_id=fetch_run_id,
        source_name=source_name,
        run_started_at=fetched_at,
    )

    raw_records: list[RawSourceRecord] = []
    canonical_records: list[CanonicalIngestionRecord] = []

    for item in items:
        run.records_fetched += 1

        raw = build_raw_record(
            item,
            fetch_run_id=fetch_run_id,
            fetched_at=fetched_at,
        )
        raw_records.append(raw)

        record = normalize_item(item, ingested_at=fetched_at)
        record.dedupe_key = compute_dedupe_key(record)

        duplicate = is_exact_duplicate(
            record,
            seen_source_keys=seen_source_keys,
            seen_content_hashes=seen_content_hashes,
        )

        if duplicate:
            record.is_duplicate = True
            run.records_duplicated += 1
            canonical_records.append(record)
            continue

        record = validate_record(record)
        canonical_records.append(record)

        seen_source_keys.add(f"{record.source_name}:{record.source_record_id}")
        seen_content_hashes.add(record.content_hash)

        if record.validation_status == "accepted":
            run.records_accepted += 1
        elif record.validation_status == "accepted_with_flags":
            run.records_accepted += 1
        elif record.validation_status == "quarantined":
            run.records_quarantined += 1
        elif record.validation_status == "rejected":
            run.records_rejected += 1

    run.run_finished_at = fetched_at
    run.run_status = "completed"
    return run, raw_records, canonical_records
