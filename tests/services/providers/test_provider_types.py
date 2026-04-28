from datetime import UTC, datetime

from app.services.providers.types import ProviderFetchResult


def test_provider_fetch_result_shape():
    fetched_at = datetime.now(UTC)

    result = ProviderFetchResult(
        provider_name="benzinga",
        fetched_at=fetched_at,
        records_returned=3,
        status="ok",
    )

    assert result.provider_name == "benzinga"
    assert result.fetched_at == fetched_at
    assert result.records_returned == 3
    assert result.status == "ok"
    assert result.error_message is None


def test_provider_fetch_result_can_include_payload():
    from datetime import UTC, datetime

    result = ProviderFetchResult(
        provider_name="market_data",
        fetched_at=datetime.now(UTC),
        records_returned=1,
        status="ok",
        payload={"symbol": "AAPL"},
    )

    assert result.payload == {"symbol": "AAPL"}
