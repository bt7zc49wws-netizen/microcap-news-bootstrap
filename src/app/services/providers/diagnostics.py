from __future__ import annotations

from collections.abc import Sequence


def aggregate_provider_status_diagnostics(diagnostics: Sequence[dict]) -> dict:
    providers = list(diagnostics)
    return {
        "provider_count": len(providers),
        "ok_count": sum(1 for item in providers if item.get("status") == "ok"),
        "error_count": sum(1 for item in providers if item.get("has_error") is True or item.get("status") == "error"),
        "has_any_payload": any(item.get("has_payload") is True for item in providers),
        "latest_fetched_at": max((item.get("fetched_at") for item in providers), default=None),
        "providers": providers,
    }


def build_live_provider_smoke_report(diagnostics: Sequence[dict], ran_at_utc: str) -> dict:
    aggregate = aggregate_provider_status_diagnostics(diagnostics)
    return {
        "status": "verified",
        "ran_at_utc": ran_at_utc,
        "provider_count": aggregate["provider_count"],
        "ok_count": aggregate["ok_count"],
        "error_count": aggregate["error_count"],
        "has_any_payload": aggregate["has_any_payload"],
        "providers": [
            {
                "provider_name": item["provider_name"],
                "status": item["status"],
                "records_returned": item["records_returned"],
                "has_error": item["has_error"],
                "has_payload": item["has_payload"],
            }
            for item in diagnostics
        ],
        "execution_side_effects": False,
        "secrets_recorded": False,
    }
