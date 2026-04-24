from datetime import datetime, timezone

from app.services.ingestion.service import process_items
from app.services.ingestion.types import ValidationStatus


def test_live_source_ingestion_flow_mixed_batch() -> None:
    now = datetime.now(timezone.utc)

    items = [
        {
            "guid": "guid-1",
            "link": "https://example.com/pr/1",
            "title": "Company Announces Registered Direct Offering",
            "content": "Financing details here.",
            "published_at": now,
            "primary_ticker": "ABCD",
            "company_name": "ABCD Therapeutics",
            "language": "en",
        },
        {
            "guid": "guid-1",
            "link": "https://example.com/pr/1-dup",
            "title": "Company Announces Registered Direct Offering",
            "content": "Financing details here.",
            "published_at": now,
            "primary_ticker": "ABCD",
            "company_name": "ABCD Therapeutics",
            "language": "en",
        },
        {
            "guid": "guid-2",
            "link": "https://example.com/pr/2",
            "title": "Company Update",
            "content": "Update body here.",
            "published_at": None,
            "primary_ticker": "WXYZ",
            "language": "en",
        },
        {
            "guid": "guid-3",
            "link": "https://example.com/pr/3",
            "title": "Company Announces Update",
            "content": "Update body here.",
            "published_at": now,
            "language": "en",
        },
        {
            "guid": "guid-4",
            "link": "https://example.com/pr/4",
            "title": "Company Announces Update",
            "content": "",
            "published_at": now,
            "primary_ticker": "ZZZZ",
            "language": "en",
        },
    ]

    run, raw_records, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.run_status == "completed"
    assert run.records_fetched == 5
    assert run.records_accepted == 2
    assert run.records_duplicated == 1
    assert run.records_quarantined == 1
    assert run.records_rejected == 1

    assert len(raw_records) == 5
    assert len(canonical_records) == 5

    by_source_id = {record.source_record_id: record for record in canonical_records}

    assert by_source_id["guid-1"].validation_status == ValidationStatus.ACCEPTED
    assert by_source_id["guid-2"].validation_status == ValidationStatus.QUARANTINED
    assert by_source_id["guid-3"].validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
    assert by_source_id["guid-4"].validation_status == ValidationStatus.REJECTED

    duplicate_records = [record for record in canonical_records if record.is_duplicate]
    assert len(duplicate_records) == 1
    assert duplicate_records[0].source_record_id == "guid-1"
