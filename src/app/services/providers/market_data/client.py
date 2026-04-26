from datetime import UTC, datetime
import csv
import urllib.request
from io import StringIO

from app.services.providers.types import ProviderFetchResult


class MarketDataClient:
    provider_name = "market_data"

    def __init__(self, provider: str, api_key: str = "") -> None:
        self.provider = provider
        self.api_key = api_key

    def fetch_snapshot(self, symbol: str) -> ProviderFetchResult:
        if self.provider == "none":
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="MARKET_DATA_PROVIDER is not configured.",
            )

        if self.provider == "stooq":
            url = f"https://stooq.com/q/l/?s={symbol.lower()}.us&f=sd2t2ohlcv&h&e=csv"
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "microcap-news-bootstrap/0.1"},
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                text = response.read().decode("utf-8")

            rows = list(csv.DictReader(StringIO(text)))
            records_returned = sum(1 for row in rows if row.get("Close") not in (None, "", "N/D"))

            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=records_returned,
                status="ok" if records_returned else "empty",
            )

        if not self.api_key:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="Market data API key is not configured.",
            )

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=0,
            status="not_implemented",
        )
