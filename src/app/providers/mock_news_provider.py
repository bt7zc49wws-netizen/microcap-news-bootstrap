from datetime import datetime, timezone


def fetch_mock_news() -> list[dict]:
    now = datetime.now(timezone.utc)
    return [
        {
            "source_name": "mock_news_provider",
            "source_type": "mock",
            "symbol": "ABCD",
            "headline": "Mock financing headline for bootstrap ingestion",
            "published_at": now,
        }
    ]
