from datetime import UTC, datetime

from app.services.providers.types import ProviderFetchResult


class BenzingaClient:
    provider_name = "benzinga"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_news(self) -> ProviderFetchResult:
        if not self.api_key:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="BENZINGA_API_KEY is not configured.",
            )

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=0,
            status="not_implemented",
        )
