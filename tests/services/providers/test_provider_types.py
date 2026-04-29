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


def test_provider_fetch_result_can_build_status_diagnostic():
    fetched_at = datetime(2026, 4, 29, 12, 0, tzinfo=UTC)
    result = ProviderFetchResult(
        provider_name="finnhub",
        fetched_at=fetched_at,
        records_returned=0,
        status="error",
        error_message="missing api key",
    )

    assert result.to_status_diagnostic() == {
        "provider_name": "finnhub",
        "status": "error",
        "records_returned": 0,
        "fetched_at": "2026-04-29T12:00:00+00:00",
        "has_error": True,
        "has_payload": False,
        "error_message": "missing api key",
    }


def test_provider_fetch_result_status_diagnostic_reports_payload_presence():
    fetched_at = datetime(2026, 4, 29, 12, 0, tzinfo=UTC)
    result = ProviderFetchResult(
        provider_name="market_data",
        fetched_at=fetched_at,
        records_returned=1,
        status="ok",
        payload={"symbol": "AAPL"},
    )

    assert result.to_status_diagnostic()["has_payload"] is True


def test_provider_fetch_result_status_diagnostic_is_json_serializable():
    fetched_at = datetime(2026, 4, 29, 12, 0, tzinfo=UTC)
    result = ProviderFetchResult(provider_name="stooq", fetched_at=fetched_at, records_returned=1, status="ok", payload={"symbol": "AAPL"})
    import json
    assert json.loads(json.dumps(result.to_status_diagnostic()))["provider_name"] == "stooq"
