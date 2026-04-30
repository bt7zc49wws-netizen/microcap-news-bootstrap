from pathlib import Path

from app.services.providers.live_smoke_report_readiness import validate_live_provider_smoke_report

REPORT_PATH = Path("reports/live_smoke/gated_live_provider_smoke_report.json")


def main() -> int:
    result = validate_live_provider_smoke_report(REPORT_PATH)
    print(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
