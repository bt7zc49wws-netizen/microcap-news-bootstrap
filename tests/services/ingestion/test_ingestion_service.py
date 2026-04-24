from datetime import datetime, timezone

from app.services.ingestion.service import process_items
from app.services.ingestion.types import ValidationStatus


def test_process_items_counts_accepted_records() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-1",
            "link": "https://example.com/pr/1",
            "title": "Company Announces Offering",
            "content": "Offering details here.",
            "published_at": now,
            "primary_ticker": "ABCD",
            "language": "en",
        }
    ]

    run, raw_records, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.records_fetched == 1
    assert run.records_accepted == 1
    assert run.records_duplicated == 0
    assert run.records_quarantined == 0
    assert run.records_rejected == 0
    assert len(raw_records) == 1
    assert len(canonical_records) == 1
    assert canonical_records[0].validation_status == ValidationStatus.ACCEPTED


def test_process_items_counts_duplicate_records() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-1",
            "link": "https://example.com/pr/1",
            "title": "Company Announces Offering",
            "content": "Offering details here.",
            "published_at": now,
            "primary_ticker": "ABCD",
            "language": "en",
        }
    ]

    run, raw_records, canonical_records = process_items(
        items,
        fetched_at=now,
        seen_source_keys={"press_release_feed_v1:guid-1"},
    )

    assert run.records_fetched == 1
    assert run.records_duplicated == 1
    assert run.records_accepted == 0
    assert len(raw_records) == 1
    assert len(canonical_records) == 1
    assert canonical_records[0].is_duplicate is True


def test_process_items_quarantines_missing_published_at() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-2",
            "link": "https://example.com/pr/2",
            "title": "Company Update",
            "content": "Update body here.",
            "published_at": None,
            "primary_ticker": "ABCD",
            "language": "en",
        }
    ]

    run, _, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.records_quarantined == 1
    assert canonical_records[0].validation_status == ValidationStatus.QUARANTINED


def test_process_items_accepts_with_flags_when_ticker_missing() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-3",
            "link": "https://example.com/pr/3",
            "title": "Company Announces Update",
            "content": "Update body here.",
            "published_at": now,
            "language": "en",
        }
    ]

    run, _, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.records_accepted == 1
    assert canonical_records[0].validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS


def test_process_items_rejects_empty_body() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-4",
            "link": "https://example.com/pr/4",
            "title": "Company Announces Update",
            "content": "",
            "published_at": now,
            "primary_ticker": "ABCD",
            "language": "en",
        }
    ]

    run, _, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.records_rejected == 1
    assert canonical_records[0].validation_status == ValidationStatus.REJECTED
