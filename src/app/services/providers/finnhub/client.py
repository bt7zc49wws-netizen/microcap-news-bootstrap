from datetime import UTC, datetime
import json
import urllib.parse
import urllib.request

from app.services.providers.types import ProviderFetchResult


class FinnhubNewsClient:
    provider_name = "finnhub"

    def __init__(self, api_key: str, http_client=None) -> None:
        self.api_key = api_key
        self.http_client = http_client or urllib.request.urlopen

    def fetch_market_news(self, category: str = "general") -> ProviderFetchResult:
        if not self.api_key:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="disabled",
                error_message="FINNHUB_API_KEY is not configured.",
            )

        query = urllib.parse.urlencode({"category": category, "token": self.api_key})
        request = urllib.request.Request(
            f"https://finnhub.io/api/v1/news?{query}",
            headers={"User-Agent": "microcap-news-bootstrap/0.1"},
        )

        try:
            with self.http_client(request, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=0,
                status="error",
                error_message=str(exc),
            )

        return ProviderFetchResult(
            provider_name=self.provider_name,
            fetched_at=datetime.now(UTC),
            records_returned=len(data) if isinstance(data, list) else 0,
            status="ok",
        )


def fetch_market_news_items(api_key: str, category: str = "general", http_client=None) -> list[dict]:
    client = FinnhubNewsClient(api_key=api_key, http_client=http_client)
    if not client.api_key:
        return []

    query = urllib.parse.urlencode({"category": category, "token": client.api_key})
    request = urllib.request.Request(
        f"https://finnhub.io/api/v1/news?{query}",
        headers={"User-Agent": "microcap-news-bootstrap/0.1"},
    )

    with client.http_client(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data if isinstance(data, list) else []


def fetch_company_news_items(
    api_key: str,
    symbol: str,
    from_date: str,
    to_date: str,
    http_client=None,
) -> list[dict]:
    client = FinnhubNewsClient(api_key=api_key, http_client=http_client)
    if not client.api_key:
        return []

    query = urllib.parse.urlencode(
        {
            "symbol": symbol,
            "from": from_date,
            "to": to_date,
            "token": client.api_key,
        }
    )
    request = urllib.request.Request(
        f"https://finnhub.io/api/v1/company-news?{query}",
        headers={"User-Agent": "microcap-news-bootstrap/0.1"},
    )

    with client.http_client(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data if isinstance(data, list) else []
