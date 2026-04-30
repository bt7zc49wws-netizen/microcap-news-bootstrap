import json
from datetime import datetime
from pathlib import Path

from app.services.providers.diagnostics import build_live_provider_smoke_report

REPORT_PATH = Path("reports/live_smoke/gated_live_provider_smoke_report.json")
REQUIRED_TOP_LEVEL_FIELDS = {
    "status",
    "ran_at_utc",
    "provider_count",
    "ok_count",
    "error_count",
    "has_any_payload",
    "providers",
    "execution_side_effects",
    "secrets_recorded",
}
REQUIRED_PROVIDER_FIELDS = {
    "provider_name",
    "status",
    "records_returned",
    "has_error",
    "has_payload",
}


def test_gated_live_provider_smoke_report_matches_contract():
    data = json.loads(REPORT_PATH.read_text())
    assert set(data) == REQUIRED_TOP_LEVEL_FIELDS
    assert data["status"] == "verified"
    assert data["secrets_recorded"] is False
    assert data["execution_side_effects"] is False
    assert isinstance(data["has_any_payload"], bool)
    assert isinstance(data["providers"], list)
    assert data["provider_count"] == len(data["providers"])
    assert data["ok_count"] + data["error_count"] == data["provider_count"]
    assert data["has_any_payload"] == any(p["has_payload"] for p in data["providers"])
    datetime.strptime(data["ran_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
    for provider in data["providers"]:
        assert set(provider) == REQUIRED_PROVIDER_FIELDS
        assert isinstance(provider["provider_name"], str) and provider["provider_name"]
        assert provider["status"] in {"ok", "error", "skipped"}
        assert isinstance(provider["records_returned"], int)
        assert provider["records_returned"] >= 0
        assert isinstance(provider["has_error"], bool)
        assert isinstance(provider["has_payload"], bool)


def test_live_provider_smoke_report_builder_matches_contract_shape() -> None:
    data = {
        "provider_name": "benzinga",
        "status": "ok",
        "records_returned": 3,
        "has_error": False,
        "has_payload": True,
        "fetched_at": "2026-04-29T12:00:00+00:00",
        "error_message": "must not leak",
    }
    report = build_live_provider_smoke_report([data], "2026-04-29T12:05:00Z")
    assert set(report) == REQUIRED_TOP_LEVEL_FIELDS
    assert set(report["providers"][0]) == REQUIRED_PROVIDER_FIELDS
    assert report["secrets_recorded"] is False
    assert report["execution_side_effects"] is False
