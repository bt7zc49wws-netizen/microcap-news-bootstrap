from app.services.providers.market_data.client import MarketDataClient, normalize_stooq_ohlcv_rows


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


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return (
            b"Symbol,Date,Time,Open,High,Low,Close,Volume\n"
            b"AAPL.US,2026-01-01,10:00:00,1,2,1,2,1000\n"
        )

def fake_http_client(request, timeout):
    return FakeResponse()


def test_market_data_client_fetches_stooq_snapshot():
    result = MarketDataClient(provider="stooq", http_client=fake_http_client).fetch_snapshot("AAPL")

    assert result.provider_name == "market_data"
    assert result.records_returned == 1
    assert result.status == "ok"
    assert result.error_message is None
    assert result.payload == [
        {
            "Symbol": "AAPL.US",
            "Date": "2026-01-01",
            "Time": "10:00:00",
            "Open": "1",
            "High": "2",
            "Low": "1",
            "Close": "2",
            "Volume": "1000",
        }
    ]


def test_normalize_stooq_ohlcv_rows_converts_csv_strings_to_quant_rows():
    rows = [
        {
            "Symbol": "AAPL.US",
            "Date": "2026-01-01",
            "Time": "10:00:00",
            "Open": "1",
            "High": "2",
            "Low": "1",
            "Close": "2",
            "Volume": "1000",
        }
    ]

    assert normalize_stooq_ohlcv_rows(rows) == [
        {
            "open": 1.0,
            "high": 2.0,
            "low": 1.0,
            "close": 2.0,
            "volume": 1000.0,
        }
    ]
