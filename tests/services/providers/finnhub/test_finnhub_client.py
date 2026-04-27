from app.services.providers.finnhub.client import FinnhubNewsClient, fetch_market_news_items


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return b'[{"id": 1}, {"id": 2}]'


def fake_http_client(request, timeout):
    return FakeResponse()


def test_finnhub_client_disabled_without_api_key():
    result = FinnhubNewsClient(api_key="").fetch_market_news()

    assert result.provider_name == "finnhub"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "FINNHUB_API_KEY is not configured."


def test_finnhub_client_fetches_market_news():
    result = FinnhubNewsClient(api_key="test-key", http_client=fake_http_client).fetch_market_news()

    assert result.provider_name == "finnhub"
    assert result.records_returned == 2
    assert result.status == "ok"
    assert result.error_message is None


def test_fetch_market_news_items_returns_raw_items():
    items = fetch_market_news_items(
        api_key="test-key",
        http_client=fake_http_client,
    )

    assert items == [{"id": 1}, {"id": 2}]
