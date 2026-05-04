import json
from pathlib import Path

from app.services.providers.diagnostics import (
    aggregate_provider_status_diagnostics,
    build_live_provider_smoke_report,
)


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


def test_aggregate_provider_status_diagnostics_preserves_provider_order() -> None:
    diagnostics = [
        {"provider_name": "first", "status": "ok", "records_returned": 1, "fetched_at": "2026-04-29T12:00:00+00:00", "has_error": False, "has_payload": True},
        {"provider_name": "second", "status": "error", "records_returned": 0, "fetched_at": "2026-04-29T12:01:00+00:00", "has_error": True, "has_payload": False},
    ]

    aggregate = aggregate_provider_status_diagnostics(diagnostics)

    assert [provider["provider_name"] for provider in aggregate["providers"]] == ["first", "second"]


def test_aggregate_provider_status_diagnostics_counts_mixed_statuses() -> None:
    diagnostics = [
        {"provider_name": "ok_a", "status": "ok", "records_returned": 1, "fetched_at": "2026-04-29T12:00:00+00:00", "has_error": False, "has_payload": True},
        {"provider_name": "err_b", "status": "error", "records_returned": 0, "fetched_at": "2026-04-29T12:01:00+00:00", "has_error": True, "has_payload": False},
        {"provider_name": "ok_c", "status": "ok", "records_returned": 2, "fetched_at": "2026-04-29T12:02:00+00:00", "has_error": False, "has_payload": True},
    ]

    aggregate = aggregate_provider_status_diagnostics(diagnostics)

    assert aggregate["provider_count"] == 3
    assert aggregate["ok_count"] == 2
    assert aggregate["error_count"] == 1
    assert aggregate["has_any_payload"] is True


def test_aggregate_provider_status_diagnostics_uses_latest_fetched_at() -> None:
    diagnostics = [
        {
            "provider_name": "older",
            "status": "ok",
            "records_returned": 1,
            "fetched_at": "2026-04-29T12:00:00+00:00",
            "has_error": False,
            "has_payload": True,
        },
        {
            "provider_name": "newer",
            "status": "ok",
            "records_returned": 1,
            "fetched_at": "2026-04-29T12:05:00+00:00",
            "has_error": False,
            "has_payload": True,
        },
    ]

    assert aggregate_provider_status_diagnostics(diagnostics)["latest_fetched_at"] == "2026-04-29T12:05:00+00:00"


def test_aggregate_provider_status_diagnostics_handles_empty_input() -> None:
    assert aggregate_provider_status_diagnostics([]) == {
        "provider_count": 0,
        "ok_count": 0,
        "error_count": 0,
        "has_any_payload": False,
        "latest_fetched_at": None,
        "providers": [],
    }


def test_aggregate_provider_status_diagnostics_matches_fixture() -> None:
    fixture_path = Path("tests/fixtures/provider_diagnostics/aggregate_provider_status_diagnostics.json")
    expected = json.loads(fixture_path.read_text())

    assert aggregate_provider_status_diagnostics(expected["providers"]) == expected


def test_build_live_provider_smoke_report_redacts_raw_payload_and_secrets() -> None:
    diagnostics = [
        {
            "provider_name": "finnhub",
            "status": "ok",
            "records_returned": 2,
            "fetched_at": "2026-04-29T12:00:00+00:00",
            "has_error": False,
            "has_payload": True,
            "error_message": "should not be copied",
        }
    ]

    assert build_live_provider_smoke_report(diagnostics, "2026-04-29T12:05:00Z") == {
        "status": "verified",
        "ran_at_utc": "2026-04-29T12:05:00Z",
        "provider_count": 1,
        "ok_count": 1,
        "error_count": 0,
        "has_any_payload": True,
        "providers": [
            {
                "provider_name": "finnhub",
                "status": "ok",
                "records_returned": 2,
                "has_error": False,
                "has_payload": True,
            }
        ],
        "execution_side_effects": False,
        "secrets_recorded": False,
    }
