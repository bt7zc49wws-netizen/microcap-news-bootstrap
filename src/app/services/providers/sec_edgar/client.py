from datetime import UTC, datetime

from app.services.providers.types import ProviderFetchResult


class SecEdgarClient:
    provider_name = "sec_edgar"

    def __init__(self, user_agent: str) -> None:
        self.user_agent = user_agent

    def fetch_company_filings(self, cik: str) -> ProviderFetchResult:
        if not self.user_agent:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="SEC_EDGAR_USER_AGENT is not configured.",
            )

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=0,
            status="not_implemented",
        )
