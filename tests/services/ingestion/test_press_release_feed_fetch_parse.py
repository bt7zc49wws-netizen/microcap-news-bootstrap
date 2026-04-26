from datetime import datetime, timezone

from app.services.ingestion.adapters.press_release_feed import (
    extract_items,
    parse_published_at,
)


def test_parse_published_at_rfc2822() -> None:
    result = parse_published_at("Thu, 24 Apr 2026 11:58:00 GMT")

    assert result == datetime(2026, 4, 24, 11, 58, 0, tzinfo=timezone.utc)


def test_parse_published_at_iso8601_zulu() -> None:
    result = parse_published_at("2026-04-24T11:58:00Z")

    assert result == datetime(2026, 4, 24, 11, 58, 0, tzinfo=timezone.utc)


def test_parse_published_at_invalid_returns_none() -> None:
    result = parse_published_at("not-a-date")

    assert result is None


def test_extract_items_from_rss_xml() -> None:
    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Example Feed</title>
        <item>
          <guid>guid-1</guid>
          <title>Company Announces Offering</title>
          <link>https://example.com/pr/1</link>
          <pubDate>Thu, 24 Apr 2026 11:58:00 GMT</pubDate>
          <description>Offering details here.</description>
        </item>
        <item>
          <guid>guid-2</guid>
          <title>Company Update</title>
          <link>https://example.com/pr/2</link>
          <pubDate>2026-04-24T12:10:00Z</pubDate>
          <description>Update details here.</description>
        </item>
      </channel>
    </rss>
    """

    items = extract_items(xml_text)

    assert len(items) == 1

    assert items[0]["guid"] == "guid-1"
    assert items[0]["title"] == "Company Announces Offering"
    assert items[0]["link"] == "https://example.com/pr/1"
    assert items[0]["description"] == "Offering details here."
    assert items[0]["published_at"] == datetime(2026, 4, 24, 11, 58, 0, tzinfo=timezone.utc)
