from app.services.providers.diagnostics import aggregate_provider_status_diagnostics


def test_aggregate_provider_status_diagnostics() -> None:
    diagnostics = [
        {
            "provider_name": "finnhub",
            "status": "ok",
            "records_returned": 2,
            "fetched_at": "2026-04-29T12:00:00+00:00",
            "has_error": False,
            "has_payload": True,
        },
        {
            "provider_name": "sec_edgar",
            "status": "error",
            "records_returned": 0,
            "fetched_at": "2026-04-29T12:01:00+00:00",
            "has_error": True,
            "has_payload": False,
            "error_message": "rate limited",
        },
    ]

    assert aggregate_provider_status_diagnostics(diagnostics) == {
        "provider_count": 2,
        "ok_count": 1,
        "error_count": 1,
        "has_any_payload": True,
        "latest_fetched_at": "2026-04-29T12:01:00+00:00",
        "providers": diagnostics,
    }
