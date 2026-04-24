from datetime import datetime, timezone

from app.services.ingestion.dedupe import compute_dedupe_key, is_exact_duplicate
from app.services.ingestion.types import CanonicalIngestionRecord, ValidationStatus


def build_record(
    *,
    source_record_id: str = "src-1",
    content_hash: str = "sha256:abc",
) -> CanonicalIngestionRecord:
    now = datetime.now(timezone.utc)
    return CanonicalIngestionRecord(
        record_id="rec-1",
        source_name="press_release_feed_v1",
        source_record_id=source_record_id,
        source_url="https://example.com/pr/1",
        title="Company Announces Offering",
        body_text="Offering details here.",
        published_at=now,
        ingested_at=now,
        processed_at=now,
        primary_ticker="ABCD",
        company_name="ABCD Therapeutics",
        language="en",
        content_hash=content_hash,
        dedupe_key="",
        is_duplicate=False,
        is_stale=False,
        validation_status=ValidationStatus.ACCEPTED,
    )


def test_compute_dedupe_key_prefers_source_identity() -> None:
    record = build_record(source_record_id="guid-123", content_hash="sha256:abc")

    result = compute_dedupe_key(record)

    assert result == "press_release_feed_v1:guid-123"


def test_compute_dedupe_key_falls_back_to_content_hash() -> None:
    record = build_record(source_record_id="", content_hash="sha256:def")

    result = compute_dedupe_key(record)

    assert result == "sha256:def"


def test_is_exact_duplicate_by_source_key() -> None:
    record = build_record(source_record_id="guid-123", content_hash="sha256:abc")

    result = is_exact_duplicate(
        record,
        seen_source_keys={"press_release_feed_v1:guid-123"},
        seen_content_hashes=set(),
    )

    assert result is True


def test_is_exact_duplicate_by_content_hash() -> None:
    record = build_record(source_record_id="guid-999", content_hash="sha256:abc")

    result = is_exact_duplicate(
        record,
        seen_source_keys=set(),
        seen_content_hashes={"sha256:abc"},
    )

    assert result is True


def test_is_exact_duplicate_false_for_new_record() -> None:
    record = build_record(source_record_id="guid-new", content_hash="sha256:new")

    result = is_exact_duplicate(
        record,
        seen_source_keys={"press_release_feed_v1:guid-old"},
        seen_content_hashes={"sha256:old"},
    )

    assert result is False
