from datetime import UTC, datetime
import csv
import urllib.request
from io import StringIO

from app.services.providers.types import ProviderFetchResult


class MarketDataClient:
    provider_name = "market_data"

    def __init__(self, provider: str, api_key: str = "", http_client=None) -> None:
        self.provider = provider
        self.api_key = api_key
        self.http_client = http_client or urllib.request.urlopen

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
            with self.http_client(request, timeout=15) as response:
                text = response.read().decode("utf-8")

            rows = list(csv.DictReader(StringIO(text)))
            valid_rows = [row for row in rows if row.get("Close") not in (None, "", "N/D")]
            records_returned = len(valid_rows)

            return ProviderFetchResult(
                provider_name=self.provider_name,
                fetched_at=datetime.now(UTC),
                records_returned=records_returned,
                status="ok" if records_returned else "empty",
                payload=valid_rows,
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

def normalize_stooq_ohlcv_rows(rows: list[dict[str, str]]) -> list[dict[str, float]]:
    """Normalize Stooq CSV rows into lowercase OHLCV rows for quant enrichment."""
    normalized: list[dict[str, float]] = []

    for row in rows:
        normalized.append(
            {
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
            }
        )

    return normalized

