from datetime import datetime, timezone

from app.services.ingestion.types import (
    CanonicalIngestionRecord,
    QualityFlag,
    ValidationStatus,
)
from app.services.ingestion.validation import validate_record


def build_record() -> CanonicalIngestionRecord:
    now = datetime.now(timezone.utc)
    return CanonicalIngestionRecord(
        record_id="rec-1",
        source_name="press_release_feed_v1",
        source_record_id="src-1",
        source_url="https://example.com/pr/1",
        title="Company Announces Offering",
        body_text="Offering details here.",
        published_at=now,
        ingested_at=now,
        processed_at=now,
        primary_ticker="ABCD",
        company_name="ABCD Therapeutics",
        language="en",
        content_hash="sha256:abc",
        dedupe_key="press_release_feed_v1:src-1",
        is_duplicate=False,
        is_stale=False,
        validation_status=ValidationStatus.ACCEPTED,
    )


def test_validate_record_accepts_clean_record() -> None:
    record = build_record()

    result = validate_record(record)

    assert result.validation_status == ValidationStatus.ACCEPTED
    assert result.quality_flags == []


def test_validate_record_rejects_empty_title() -> None:
    record = build_record()
    record.title = "   "

    result = validate_record(record)

    assert result.validation_status == ValidationStatus.REJECTED


def test_validate_record_rejects_empty_body() -> None:
    record = build_record()
    record.body_text = "   "

    result = validate_record(record)

    assert result.validation_status == ValidationStatus.REJECTED


def test_validate_record_quarantines_missing_published_at() -> None:
    record = build_record()
    record.published_at = None

    result = validate_record(record)

    assert result.validation_status == ValidationStatus.QUARANTINED
    assert QualityFlag.PARTIAL_PARSE in result.quality_flags


def test_validate_record_accepts_with_existing_flags() -> None:
    record = build_record()
    record.quality_flags = [QualityFlag.TICKER_MISSING]

    result = validate_record(record)

    assert result.validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
    assert QualityFlag.TICKER_MISSING in result.quality_flags
