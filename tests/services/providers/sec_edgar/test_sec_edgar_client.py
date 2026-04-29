from app.services.providers.sec_edgar.client import SecEdgarClient


def test_sec_edgar_client_disabled_without_user_agent():
    result = SecEdgarClient(user_agent="").fetch_company_filings("0000320193")

    assert result.provider_name == "sec_edgar"
    assert result.records_returned == 0
    assert result.status == "disabled"
    assert result.error_message == "SEC_EDGAR_USER_AGENT is not configured."


def test_sec_edgar_client_fetches_company_filings_with_user_agent(monkeypatch):
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): return None
        def read(self): return b"{\"filings\":{\"recent\":{\"accessionNumber\":[\"a\",\"b\"]}}}"
    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: FakeResponse())
    result = SecEdgarClient(user_agent="test@example.com").fetch_company_filings("0000320193")

    assert result.provider_name == "sec_edgar"
    assert result.records_returned > 0
    assert result.status == "ok"
    assert result.error_message is None
