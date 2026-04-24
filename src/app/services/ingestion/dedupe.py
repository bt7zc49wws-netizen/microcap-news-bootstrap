from __future__ import annotations

from app.services.ingestion.types import CanonicalIngestionRecord


def compute_dedupe_key(record: CanonicalIngestionRecord) -> str:
    if record.source_record_id:
        return f"{record.source_name}:{record.source_record_id}"
    return record.content_hash


def is_exact_duplicate(
    record: CanonicalIngestionRecord,
    *,
    seen_source_keys: set[str],
    seen_content_hashes: set[str],
) -> bool:
    source_key = f"{record.source_name}:{record.source_record_id}"

    if source_key in seen_source_keys:
        return True

    if record.content_hash in seen_content_hashes:
        return True

    return False
