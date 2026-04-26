from app.services.providers.sec_edgar.client import SecEdgarClient


def test_sec_edgar_client_disabled_without_user_agent():
    result = SecEdgarClient(user_agent="").fetch_company_filings("0000320193")

    assert result.provider_name == "sec_edgar"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "SEC_EDGAR_USER_AGENT is not configured."


def test_sec_edgar_client_not_implemented_with_user_agent():
    result = SecEdgarClient(user_agent="test@example.com").fetch_company_filings("0000320193")

    assert result.provider_name == "sec_edgar"
    assert result.records_returned == 0
    assert result.status == "not_implemented"
    assert result.error_message is None
