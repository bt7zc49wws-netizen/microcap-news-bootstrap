import os

from app.services.providers.finnhub.client import FinnhubNewsClient
from app.services.providers.fundamentals.client import FundamentalsClient
from app.services.providers.market_data.client import MarketDataClient
from app.services.providers.sec_edgar.client import SecEdgarClient


def main() -> None:
    if os.getenv("ENABLE_FREE_PROVIDER_SMOKE") != "1":
        print("free provider smoke skipped: ENABLE_FREE_PROVIDER_SMOKE is not set")
        return

    finnhub_key = os.getenv("FINNHUB_API_KEY", "")
    if not finnhub_key:
        print("free provider smoke skipped: FINNHUB_API_KEY is not set")
        return
    print(FinnhubNewsClient(api_key=finnhub_key).fetch_market_news().to_status_diagnostic())
    print(SecEdgarClient(user_agent="test@example.com").fetch_company_filings("0000320193").to_status_diagnostic())
    print(MarketDataClient(provider="stooq").fetch_snapshot("AAPL").to_status_diagnostic())
    print(FundamentalsClient(provider="stooq").fetch_company_profile("AAPL").to_status_diagnostic())


if __name__ == "__main__":
    main()
