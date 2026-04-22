from datetime import datetime, timedelta, timezone


def fetch_mock_news() -> list[dict]:
    now = datetime.now(timezone.utc)
    return [
        {
            "external_id": "mock-news-001",
            "source_name": "mock_news_provider",
            "source_type": "mock",
            "symbol": "ABCD",
            "headline": "Mock financing headline for bootstrap ingestion",
            "source_event_time": now - timedelta(minutes=2),
            "published_at": now - timedelta(minutes=1),
            "quality_flags": '["mock_source"]',
        },
        {
            "external_id": "mock-news-002",
            "source_name": "mock_news_provider",
            "source_type": "mock",
            "symbol": "WXYZ",
            "headline": "Mock offering update for ingestion pipeline",
            "source_event_time": now - timedelta(minutes=1),
            "published_at": now,
            "quality_flags": '["mock_source"]',
        },
    ]
