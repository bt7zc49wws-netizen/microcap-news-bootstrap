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

    def get(self, url: str, timeout: int = 15) -> DummyResponse:
        return DummyResponse(self.response_text)


def test_run_live_ingestion_smoke() -> None:
    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <item>
          <guid>guid-1</guid>
          <title>Company Announces Registered Direct Offering</title>
          <link>https://example.com/pr/1</link>
          <pubDate>Thu, 24 Apr 2026 11:58:00 GMT</pubDate>
          <description>Financing details here.</description>
        </item>
      </channel>
    </rss>
    """

    config = IngestionConfig(
        live_source_enabled=True,
        live_source_url="https://example.com/feed.xml",
        live_source_timeout_seconds=10,
        live_source_max_items_per_run=10,
    )

    run, raw_records, canonical_records = run_live_ingestion(
        config,
        http_client=DummyHttpClient(xml_text),
    )

    assert run.run_status == "completed"
    assert run.records_fetched == 1
    assert len(raw_records) == 1
    assert len(canonical_records) == 1
    assert canonical_records[0].source_record_id == "guid-1"
