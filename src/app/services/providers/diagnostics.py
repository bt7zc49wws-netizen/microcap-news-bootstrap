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
