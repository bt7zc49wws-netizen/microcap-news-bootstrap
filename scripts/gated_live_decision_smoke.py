import os

from app.services.providers.finnhub.client import FinnhubNewsClient
from app.services.providers.fundamentals.client import FundamentalsClient
from app.services.providers.market_data.client import MarketDataClient
from app.services.providers.sec_edgar.client import SecEdgarClient


def main() -> None:
    if os.getenv("ENABLE_GATED_LIVE_SMOKE") != "1":
        print("gated live decision smoke skipped: ENABLE_GATED_LIVE_SMOKE is not set")
        return

    finnhub_key = os.getenv("FINNHUB_API_KEY", "")
    sec_user_agent = os.getenv("SEC_EDGAR_USER_AGENT", "test@example.com")
    symbol = os.getenv("GATED_LIVE_SMOKE_SYMBOL", "AAPL")
    cik = os.getenv("GATED_LIVE_SMOKE_CIK", "0000320193")

    print(FinnhubNewsClient(api_key=finnhub_key).fetch_market_news())
    print(SecEdgarClient(user_agent=sec_user_agent).fetch_company_filings(cik))
    print(MarketDataClient(provider="stooq").fetch_snapshot(symbol))
    print(FundamentalsClient(provider="stooq").fetch_company_profile(symbol))
    print("gated live decision smoke completed without execution side effects")


if __name__ == "__main__":
    main()
