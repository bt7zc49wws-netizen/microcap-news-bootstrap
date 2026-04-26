from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True, slots=True)
class IngestionConfig:
    live_source_enabled: bool = False
    live_source_url: str = ""
    live_source_poll_interval_seconds: int = 300
    live_source_timeout_seconds: int = 15
    live_source_max_items_per_run: int = 100
    live_source_staleness_threshold_seconds: int = 72 * 3600


def _as_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def load_ingestion_config() -> IngestionConfig:
    return IngestionConfig(
        live_source_enabled=_as_bool(os.getenv("LIVE_SOURCE_ENABLED"), default=False),
        live_source_url=os.getenv("LIVE_SOURCE_URL", ""),
        live_source_poll_interval_seconds=int(os.getenv("LIVE_SOURCE_POLL_INTERVAL_SECONDS", "300")),
        live_source_timeout_seconds=int(os.getenv("LIVE_SOURCE_TIMEOUT_SECONDS", "15")),
        live_source_max_items_per_run=int(os.getenv("LIVE_SOURCE_MAX_ITEMS_PER_RUN", "100")),
        live_source_staleness_threshold_seconds=int(
            os.getenv("LIVE_SOURCE_STALENESS_THRESHOLD_SECONDS", str(72 * 3600))
        ),
    )


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    benzinga_api_key: str = ""
    market_data_provider: str = "none"
    polygon_api_key: str = ""
    tiingo_api_key: str = ""
    sec_edgar_user_agent: str = ""
    fundamentals_provider: str = "none"
    finnhub_api_key: str = ""
    fmp_api_key: str = ""


def load_provider_config() -> ProviderConfig:
    return ProviderConfig(
        benzinga_api_key=os.getenv("BENZINGA_API_KEY", ""),
        market_data_provider=os.getenv("MARKET_DATA_PROVIDER", "none"),
        polygon_api_key=os.getenv("POLYGON_API_KEY", ""),
        tiingo_api_key=os.getenv("TIINGO_API_KEY", ""),
        sec_edgar_user_agent=os.getenv("SEC_EDGAR_USER_AGENT", ""),
        fundamentals_provider=os.getenv("FUNDAMENTALS_PROVIDER", "none"),
        finnhub_api_key=os.getenv("FINNHUB_API_KEY", ""),
        fmp_api_key=os.getenv("FMP_API_KEY", ""),
    )
