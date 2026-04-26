from datetime import UTC, datetime
import json
import urllib.request

from app.services.providers.types import ProviderFetchResult


class FundamentalsClient:
    provider_name = "fundamentals"

    def __init__(self, provider: str, api_key: str = "") -> None:
        self.provider = provider
        self.api_key = api_key

    def fetch_company_profile(self, symbol: str) -> ProviderFetchResult:
        if self.provider == "none":
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="FUNDAMENTALS_PROVIDER is not configured.",
            )

        if self.provider == "stooq":
            url = f"https://stooq.com/q/l/?s={symbol.lower()}.us&f=sd2t2ohlcv&h&e=json"
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "microcap-news-bootstrap/0.1"},
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                json.loads(response.read().decode("utf-8"))

            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=1,
                status="ok",
            )

        if not self.api_key:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="Fundamentals API key is not configured.",
            )

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=0,
            status="not_implemented",
        )
