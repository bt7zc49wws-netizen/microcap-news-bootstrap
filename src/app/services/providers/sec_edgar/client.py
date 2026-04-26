from datetime import UTC, datetime
import json
import urllib.request

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

        normalized_cik = cik.zfill(10)
        request = urllib.request.Request(
            f"https://data.sec.gov/submissions/CIK{normalized_cik}.json",
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="error",
                error_message=str(exc),
            )

        recent = payload.get("filings", {}).get("recent", {})
        accession_numbers = recent.get("accessionNumber", [])

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=len(accession_numbers),
            status="ok",
        )
