import os

from app.services.providers.finnhub.client import FinnhubNewsClient
from app.services.providers.fundamentals.client import FundamentalsClient
from app.services.providers.market_data.client import MarketDataClient
from app.services.providers.sec_edgar.client import SecEdgarClient


def main() -> None:
    finnhub_key = os.getenv("FINNHUB_API_KEY", "")
    print(FinnhubNewsClient(api_key=finnhub_key).fetch_market_news())
    print(SecEdgarClient(user_agent="test@example.com").fetch_company_filings("0000320193"))
    print(MarketDataClient(provider="stooq").fetch_snapshot("AAPL"))
    print(FundamentalsClient(provider="stooq").fetch_company_profile("AAPL"))


if __name__ == "__main__":
    main()
