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
