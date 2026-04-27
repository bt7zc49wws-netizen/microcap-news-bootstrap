from datetime import UTC, datetime

from app.services.ingestion.adapters.finnhub_news import normalize_finnhub_news_item
from app.services.ingestion.types import ValidationStatus


def test_normalize_finnhub_news_item():
    ingested_at = datetime(2026, 1, 1, tzinfo=UTC)

    record = normalize_finnhub_news_item(
        {
            "id": 123,
            "headline": "Company Announces Financing",
            "summary": "Company raised capital.",
            "url": "https://example.com/news/123",
            "related": "ABCD",
            "datetime": 1767225600,
        },
        ingested_at=ingested_at,
    )

    assert record.source_name == "finnhub_news"
    assert record.source_record_id == "123"
    assert record.title == "Company Announces Financing"
    assert record.body_text == "Company raised capital."
    assert record.primary_ticker == "ABCD"
    assert record.validation_status == ValidationStatus.ACCEPTED
