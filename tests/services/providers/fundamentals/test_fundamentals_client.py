from app.services.providers.fundamentals.client import FundamentalsClient


def test_fundamentals_client_disabled_without_provider():
    result = FundamentalsClient(provider="none").fetch_company_profile("ABCD")

    assert result.provider_name == "fundamentals"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "FUNDAMENTALS_PROVIDER is not configured."


def test_fundamentals_client_disabled_without_api_key():
    result = FundamentalsClient(provider="fmp", api_key="").fetch_company_profile("ABCD")

    assert result.provider_name == "fundamentals"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "Fundamentals API key is not configured."


def test_fundamentals_client_not_implemented_with_api_key():
    result = FundamentalsClient(provider="fmp", api_key="test-key").fetch_company_profile("ABCD")

    assert result.provider_name == "fundamentals"
    assert result.records_returned == 0
    assert result.status == "not_implemented"
    assert result.error_message is None
