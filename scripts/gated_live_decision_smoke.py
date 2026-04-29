import os

from app.services.providers.finnhub.client import FinnhubNewsClient
from app.services.providers.fundamentals.client import FundamentalsClient
from app.services.providers.market_data.client import MarketDataClient
from app.services.providers.sec_edgar.client import SecEdgarClient
from app.services.providers.diagnostics import aggregate_provider_status_diagnostics


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
    print(aggregate_provider_status_diagnostics(diagnostics))
    print("gated live decision smoke completed without execution side effects")


if __name__ == "__main__":
    main()
