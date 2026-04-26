from datetime import UTC, datetime

from app.classification.rules import classify_record
from app.models.ingestion_record import IngestionRecord


def make_record(headline: str) -> IngestionRecord:
    now = datetime.now(UTC)
    return IngestionRecord(
        record_id="test-record",
        external_id="test-external",
        source_name="test",
        source_type="live",
        symbol="ABCD",
        headline=headline,
        source_event_time=now,
        published_at=now,
        ingested_at=now,
        processed_at=now,
        status="accepted",
        quality_flags="[]",
        is_duplicate=False,
    )


def test_classifies_financing_keyword():
    result = classify_record(make_record("Company Announces Financing"))
    assert result["classification_status"] == "EVENT_CANDIDATE"
    assert result["event_family"] == "financing"


def test_classifies_offering_keyword():
    result = classify_record(make_record("Company Announces Public Offering"))
    assert result["classification_status"] == "EVENT_CANDIDATE"
    assert result["event_family"] == "financing"


def test_low_priority_without_clear_event():
    result = classify_record(make_record("Company Announces Investor Conference"))
    assert result["classification_status"] == "LOW_PRIORITY_CANDIDATE"


def test_classifies_registered_direct_offering():
    result = classify_record(make_record("Company Announces Registered Direct Offering"))
    assert result["classification_status"] == "EVENT_CANDIDATE"
    assert result["event_family"] == "financing"


def test_classifies_convertible_note_financing():
    result = classify_record(make_record("Company Enters Into Convertible Note Purchase Agreement"))
    assert result["classification_status"] == "EVENT_CANDIDATE"
    assert result["event_family"] == "financing"


def test_classifies_warrant_financing_language():
    result = classify_record(make_record("Company Announces Exercise of Warrants for Gross Proceeds"))
    assert result["classification_status"] == "EVENT_CANDIDATE"
    assert result["event_family"] == "financing"
