import json
from pathlib import Path

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


def validate_live_provider_smoke_report(path: Path) -> dict:
    data = json.loads(path.read_text())
    if set(data) != REQUIRED_TOP_LEVEL_FIELDS:
        return {"ok": False, "reason": "top_level_fields_mismatch"}
    if data["secrets_recorded"] is not False:
        return {"ok": False, "reason": "secrets_recorded"}
    if data["execution_side_effects"] is not False:
        return {"ok": False, "reason": "execution_side_effects"}
    if data["provider_count"] != len(data["providers"]):
        return {"ok": False, "reason": "provider_count_mismatch"}
    if data["ok_count"] + data["error_count"] != data["provider_count"]:
        return {"ok": False, "reason": "aggregate_count_mismatch"}
    for provider in data["providers"]:
        if set(provider) != REQUIRED_PROVIDER_FIELDS:
            return {"ok": False, "reason": "provider_fields_mismatch"}
    if data["has_any_payload"] != any(provider["has_payload"] for provider in data["providers"]):
        return {"ok": False, "reason": "payload_flag_mismatch"}
    return {"ok": True, "reason": "ok"}
