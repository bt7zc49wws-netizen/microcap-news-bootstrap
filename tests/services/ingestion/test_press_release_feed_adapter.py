from datetime import datetime, timezone

from app.services.ingestion.adapters.press_release_feed import (
    ADAPTER_VERSION,
    NORMALIZATION_VERSION,
    SOURCE_NAME,
    build_raw_record,
    compute_content_hash,
    normalize_item,
)
from app.services.ingestion.types import QualityFlag, ValidationStatus


def test_compute_content_hash_is_stable() -> None:
    left = compute_content_hash(
        title="Company Announces Offering",
        body_text="Offering details here.",
    )
    right = compute_content_hash(
        title="Company Announces Offering",
        body_text="Offering details here.",
    )

    assert left == right
    assert left.startswith("sha256:")


def test_build_raw_record_uses_guid_when_present() -> None:
    now = datetime.now(timezone.utc)

    item = {
        "guid": "guid-123",
        "link": "https://example.com/pr/123",
        "title": "Company Announces Offering",
        "content": "Offering details here.",
    }

    raw = build_raw_record(
        item,
        fetch_run_id="run-1",
        fetched_at=now,
    )

    assert raw.source_name == SOURCE_NAME
    assert raw.source_record_id == "guid-123"
    assert raw.fetch_run_id == "run-1"
    assert raw.fetched_at == now
    assert raw.source_url == "https://example.com/pr/123"
    assert raw.raw_payload == item
    assert raw.adapter_version == ADAPTER_VERSION
    assert raw.content_hash.startswith("sha256:")


def test_normalize_item_without_ticker_sets_flag() -> None:
    now = datetime.now(timezone.utc)

    item = {
        "guid": "guid-123",
        "link": "https://example.com/pr/123",
        "title": "Company Announces Offering",
        "content": "Offering details here.",
        "published_at": now,
        "language": "en",
    }

    record = normalize_item(item, ingested_at=now)

    assert record.source_name == SOURCE_NAME
    assert record.source_record_id == "guid-123"
    assert record.dedupe_key == "press_release_feed_v1:guid-123"
    assert record.validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
    assert QualityFlag.TICKER_MISSING in record.quality_flags
    assert record.normalization_version == NORMALIZATION_VERSION


def test_normalize_item_description_only_sets_flag() -> None:
    now = datetime.now(timezone.utc)

    item = {
        "guid": "guid-456",
        "link": "https://example.com/pr/456",
        "title": "Company Update",
        "description": "Body from description only.",
        "published_at": now,
        "primary_ticker": "ABCD",
        "language": "en",
    }

    record = normalize_item(item, ingested_at=now)

    assert record.source_record_id == "guid-456"
    assert record.body_text == "Body from description only."
    assert record.validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
    assert QualityFlag.BODY_FROM_DESCRIPTION in record.quality_flags
    assert QualityFlag.TICKER_MISSING not in record.quality_flags


def test_normalize_item_with_ticker_and_content_is_accepted() -> None:
    now = datetime.now(timezone.utc)

    item = {
        "guid": "guid-789",
        "link": "https://example.com/pr/789",
        "title": "Company Announces Registered Direct Offering",
        "content": "Financing details here.",
        "published_at": now,
        "primary_ticker": "ABCD",
        "company_name": "ABCD Therapeutics",
        "language": "en",
    }

    record = normalize_item(item, ingested_at=now)

    assert record.title == "Company Announces Registered Direct Offering"
    assert record.body_text == "Financing details here."
    assert record.primary_ticker == "ABCD"
    assert record.company_name == "ABCD Therapeutics"
    assert record.validation_status == ValidationStatus.ACCEPTED
    assert record.quality_flags == []
