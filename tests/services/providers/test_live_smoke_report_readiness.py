import json
from pathlib import Path

from app.services.providers.live_smoke_report_readiness import validate_live_provider_smoke_report


def _write_report(path: Path, overrides: dict | None = None) -> None:
    data = {
        "status": "verified",
        "ran_at_utc": "2026-04-29T12:05:00Z",
        "provider_count": 1,
        "ok_count": 1,
        "error_count": 0,
        "has_any_payload": True,
        "providers": [
            {
                "provider_name": "benzinga",
                "status": "ok",
                "records_returned": 3,
                "has_error": False,
                "has_payload": True,
            }
        ],
        "execution_side_effects": False,
        "secrets_recorded": False,
    }
    if overrides:
        data.update(overrides)
    path.write_text(json.dumps(data))


def test_validate_live_provider_smoke_report_accepts_contract_report(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    _write_report(report_path)

    assert validate_live_provider_smoke_report(report_path) == {"ok": True, "reason": "ok"}


def test_validate_live_provider_smoke_report_rejects_secret_recording(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    _write_report(report_path, {"secrets_recorded": True})

    assert validate_live_provider_smoke_report(report_path) == {"ok": False, "reason": "secrets_recorded"}


def test_validate_live_provider_smoke_report_rejects_provider_field_drift(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    _write_report(report_path, {"providers": [{"provider_name": "benzinga"}]})

    assert validate_live_provider_smoke_report(report_path) == {"ok": False, "reason": "provider_fields_mismatch"}
