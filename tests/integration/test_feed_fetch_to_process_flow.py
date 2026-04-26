from datetime import datetime, timezone

from app.services.ingestion.adapters.press_release_feed import extract_items
from app.services.ingestion.service import process_items
from app.services.ingestion.types import ValidationStatus


def test_feed_fetch_to_process_flow() -> None:
    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Example Feed</title>
        <item>
          <guid>guid-1</guid>
          <title>Company Announces Registered Direct Offering</title>
          <link>https://example.com/pr/1</link>
          <pubDate>Thu, 24 Apr 2026 11:58:00 GMT</pubDate>
          <description>Financing details here.</description>
        </item>
        <item>
          <guid>guid-2</guid>
          <title>Company Update</title>
          <link>https://example.com/pr/2</link>
          <pubDate>2026-04-24T12:10:00Z</pubDate>
          <description>General update text.</description>
        </item>
      </channel>
    </rss>
    """

    items = extract_items(xml_text)
    now = datetime.now(timezone.utc)

    run, raw_records, canonical_records = process_items(
        items,
        fetched_at=now,
    )

    assert run.run_status == "completed"
    assert run.records_fetched == 1
    assert run.records_accepted == 1
    assert run.records_duplicated == 0
    assert run.records_quarantined == 0
    assert run.records_rejected == 0

    assert len(raw_records) == 1
    assert len(canonical_records) == 1

    assert canonical_records[0].source_record_id == "guid-1"
    assert canonical_records[0].validation_status == ValidationStatus.ACCEPTED_WITH_FLAGS
