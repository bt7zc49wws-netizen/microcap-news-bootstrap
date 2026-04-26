from datetime import UTC, datetime

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
