from app.services.ingestion.adapters.press_release_feed import fetch_feed


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


def test_fetch_feed_uses_http_client_and_returns_text() -> None:
    client = DummyHttpClient("<rss><channel></channel></rss>")

    result = fetch_feed(
        "https://example.com/feed.xml",
        http_client=client,
        timeout=15,
    )

    assert result == "<rss><channel></channel></rss>"
    assert client.requested_urls == ["https://example.com/feed.xml"]
