from datetime import datetime, timezone

from app.services.ingestion.types import (
    CanonicalIngestionRecord,
    FetchRun,
    QualityFlag,
    RawSourceRecord,
    ValidationStatus,
)


def test_validation_status_values() -> None:
    assert ValidationStatus.ACCEPTED == "accepted"
    assert ValidationStatus.ACCEPTED_WITH_FLAGS == "accepted_with_flags"
    assert ValidationStatus.QUARANTINED == "quarantined"
    assert ValidationStatus.REJECTED == "rejected"


def test_fetch_run_defaults() -> None:
    now = datetime.now(timezone.utc)

    run = FetchRun(
        fetch_run_id="run-1",
        source_name="press_release_feed_v1",
        run_started_at=now,
    )

    assert run.fetch_run_id == "run-1"
    assert run.source_name == "press_release_feed_v1"
    assert run.run_started_at == now
    assert run.run_finished_at is None
    assert run.run_status == "started"
    assert run.records_fetched == 0
    assert run.records_accepted == 0
    assert run.records_rejected == 0
    assert run.records_quarantined == 0
    assert run.records_duplicated == 0
    assert run.error_summary is None


def test_raw_source_record_fields() -> None:
    now = datetime.now(timezone.utc)

    raw = RawSourceRecord(
        raw_record_id="raw-1",
        source_name="press_release_feed_v1",
        source_record_id="src-1",
        fetch_run_id="run-1",
        fetched_at=now,
        source_url="https://example.com/pr/1",
        raw_payload={"title": "Example"},
        content_hash="sha256:abc",
        adapter_version="press_release_feed_adapter_v1",
    )

    assert raw.raw_record_id == "raw-1"
    assert raw.source_name == "press_release_feed_v1"
    assert raw.source_record_id == "src-1"
    assert raw.fetch_run_id == "run-1"
    assert raw.fetched_at == now
    assert raw.source_url == "https://example.com/pr/1"
    assert raw.raw_payload["title"] == "Example"
    assert raw.content_hash == "sha256:abc"
    assert raw.adapter_version == "press_release_feed_adapter_v1"


def test_canonical_ingestion_record_defaults() -> None:
    now = datetime.now(timezone.utc)

    record = CanonicalIngestionRecord(
        record_id="rec-1",
        source_name="press_release_feed_v1",
        source_record_id="src-1",
        source_url="https://example.com/pr/1",
        title="Company Announces Registered Direct Offering",
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

    assert record.record_id == "rec-1"
    assert record.validation_status == ValidationStatus.ACCEPTED
    assert record.quality_flags == []
    assert record.raw_record_ref is None
    assert record.normalization_version == "canonical_ingest_v1"


def test_canonical_ingestion_record_quality_flags() -> None:
    now = datetime.now(timezone.utc)

    record = CanonicalIngestionRecord(
        record_id="rec-2",
        source_name="press_release_feed_v1",
        source_record_id="src-2",
        source_url=None,
        title="Company Update",
        body_text="Body from description only.",
        published_at=None,
        ingested_at=now,
        processed_at=now,
        primary_ticker=None,
        company_name=None,
        language="en",
        content_hash="sha256:def",
        dedupe_key="sha256:def",
        is_duplicate=False,
        is_stale=True,
        validation_status=ValidationStatus.ACCEPTED_WITH_FLAGS,
        quality_flags=[
            QualityFlag.TICKER_MISSING,
            QualityFlag.BODY_FROM_DESCRIPTION,
            QualityFlag.STALE_RECORD,
        ],
        raw_record_ref="raw-2",
    )

    assert record.validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
    assert QualityFlag.TICKER_MISSING in record.quality_flags
    assert QualityFlag.BODY_FROM_DESCRIPTION in record.quality_flags
    assert QualityFlag.STALE_RECORD in record.quality_flags
    assert record.raw_record_ref == "raw-2"
