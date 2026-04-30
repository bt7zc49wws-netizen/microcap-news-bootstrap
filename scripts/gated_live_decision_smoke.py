import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.services.providers.finnhub.client import FinnhubNewsClient
from app.services.providers.fundamentals.client import FundamentalsClient
from app.services.providers.market_data.client import MarketDataClient
from app.services.providers.sec_edgar.client import SecEdgarClient
from app.services.providers.diagnostics import (
    aggregate_provider_status_diagnostics,
    build_live_provider_smoke_report,
)

REPORT_PATH = Path("reports/live_smoke/gated_live_provider_smoke_report.json")


def main() -> None:
    if os.getenv("ENABLE_GATED_LIVE_SMOKE") != "1":
        print("gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set")
        return

    finnhub_key = os.getenv("FINNHUB_API_KEY", "")
    if not finnhub_key:
        print("gated live decision smoke skipped: FINNHUB_API_KEY is not set")
        return
    sec_user_agent = os.getenv("SEC_EDGAR_USER_AGENT", "")
    if not sec_user_agent:
        print("gated live decision smoke skipped: SEC_EDGAR_USER_AGENT is not set")
        return
    if sec_user_agent == "test@example.com":
        print("gated live decision smoke skipped: SEC_EDGAR_USER_AGENT must be a real contact string")
        return
    symbol = os.getenv("GATED_LIVE_SMOKE_SYMBOL", "AAPL")
    cik = os.getenv("GATED_LIVE_SMOKE_CIK", "0000320193")

    diagnostics = [
        FinnhubNewsClient(api_key=finnhub_key).fetch_market_news().to_status_diagnostic(),
        SecEdgarClient(user_agent=sec_user_agent).fetch_company_filings(cik).to_status_diagnostic(),
        MarketDataClient(provider="stooq").fetch_snapshot(symbol).to_status_diagnostic(),
        FundamentalsClient(provider="stooq").fetch_company_profile(symbol).to_status_diagnostic(),
    ]
    for diagnostic in diagnostics:
        print(diagnostic)
    aggregate = aggregate_provider_status_diagnostics(diagnostics)
    report = build_live_provider_smoke_report(
        diagnostics,
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(aggregate)
    print(f"gated live provider smoke report written: {REPORT_PATH}")
    print("gated live decision smoke completed without execution side effects")


if __name__ == "__main__":
    main()
