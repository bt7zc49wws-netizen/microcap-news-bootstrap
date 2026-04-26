from app.services.providers.market_data.client import MarketDataClient


def test_market_data_client_disabled_without_provider():
    result = MarketDataClient(provider="none").fetch_snapshot("ABCD")

    assert result.provider_name == "market_data"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "MARKET_DATA_PROVIDER is not configured."


def test_market_data_client_disabled_without_api_key():
    result = MarketDataClient(provider="polygon", api_key="").fetch_snapshot("ABCD")

    assert result.provider_name == "market_data"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "Market data API key is not configured."


def test_market_data_client_not_implemented_with_api_key():
    result = MarketDataClient(provider="polygon", api_key="test-key").fetch_snapshot("ABCD")

    assert result.provider_name == "market_data"
    assert result.records_returned == 0
    assert result.status == "not_implemented"
    assert result.error_message is None


def test_market_data_client_fetches_stooq_snapshot():
    result = MarketDataClient(provider="stooq").fetch_snapshot("AAPL")

    assert result.provider_name == "market_data"
    assert result.records_returned >= 0
    assert result.status in {"ok", "empty"}
    assert result.error_message is None
