from app.services.providers.benzinga.client import BenzingaClient


def test_benzinga_client_disabled_without_api_key():
    result = BenzingaClient(api_key="").fetch_news()

    assert result.provider_name == "benzinga"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "BENZINGA_API_KEY is not configured."


def test_benzinga_client_not_implemented_with_api_key():
    result = BenzingaClient(api_key="test-key").fetch_news()

    assert result.provider_name == "benzinga"
    assert result.records_returned == 0
    assert result.status == "not_implemented"
    assert result.error_message is None
