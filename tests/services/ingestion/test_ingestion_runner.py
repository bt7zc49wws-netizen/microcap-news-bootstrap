from app.services.ingestion.config import IngestionConfig
from app.services.ingestion.runner import run_live_ingestion


class DummyResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


class DummyHttpClient:
    def __init__(self, response_text: str) -> None:
        self.response_text = response_text
        self.requested_urls: list[str] = []

    def get(self, url: str, timeout: int = 15) -> DummyResponse:
        self.requested_urls.append(url)
        return DummyResponse(self.response_text)


def test_run_live_ingestion_raises_when_disabled() -> None:
    config = IngestionConfig(
        live_source_enabled=False,
        live_source_url="https://example.com/feed.xml",
    )

    try:
        run_live_ingestion(config)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Live source ingestion is disabled."


def test_run_live_ingestion_raises_when_url_missing() -> None:
    config = IngestionConfig(
        live_source_enabled=True,
        live_source_url="   ",
    )

    try:
        run_live_ingestion(config)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "LIVE_SOURCE_URL must be set when live ingestion is enabled."


def test_run_live_ingestion_fetches_and_processes_feed() -> None:
    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
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

    client = DummyHttpClient(xml_text)
    config = IngestionConfig(
        live_source_enabled=True,
        live_source_url="https://example.com/feed.xml",
        live_source_timeout_seconds=9,
        live_source_max_items_per_run=1,
    )

    run, raw_records, canonical_records = run_live_ingestion(
        config,
        http_client=client,
        persist=False,
    )

    assert client.requested_urls == ["https://example.com/feed.xml"]
    assert run.run_status == "completed"
    assert run.records_fetched == 1
    assert len(raw_records) == 1
    assert len(canonical_records) == 1
    assert canonical_records[0].source_record_id == "guid-1"
