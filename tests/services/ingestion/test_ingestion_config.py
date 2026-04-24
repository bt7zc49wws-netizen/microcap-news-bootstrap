from app.services.ingestion.config import IngestionConfig, load_ingestion_config


def test_load_ingestion_config_defaults(monkeypatch) -> None:
    monkeypatch.delenv("LIVE_SOURCE_ENABLED", raising=False)
    monkeypatch.delenv("LIVE_SOURCE_URL", raising=False)
    monkeypatch.delenv("LIVE_SOURCE_POLL_INTERVAL_SECONDS", raising=False)
    monkeypatch.delenv("LIVE_SOURCE_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("LIVE_SOURCE_MAX_ITEMS_PER_RUN", raising=False)
    monkeypatch.delenv("LIVE_SOURCE_STALENESS_THRESHOLD_SECONDS", raising=False)

    config = load_ingestion_config()

    assert config == IngestionConfig(
        live_source_enabled=False,
        live_source_url="",
        live_source_poll_interval_seconds=300,
        live_source_timeout_seconds=15,
        live_source_max_items_per_run=100,
        live_source_staleness_threshold_seconds=72 * 3600,
    )


def test_load_ingestion_config_from_env(monkeypatch) -> None:
    monkeypatch.setenv("LIVE_SOURCE_ENABLED", "true")
    monkeypatch.setenv("LIVE_SOURCE_URL", "https://example.com/feed.xml")
    monkeypatch.setenv("LIVE_SOURCE_POLL_INTERVAL_SECONDS", "120")
    monkeypatch.setenv("LIVE_SOURCE_TIMEOUT_SECONDS", "9")
    monkeypatch.setenv("LIVE_SOURCE_MAX_ITEMS_PER_RUN", "25")
    monkeypatch.setenv("LIVE_SOURCE_STALENESS_THRESHOLD_SECONDS", "3600")

    config = load_ingestion_config()

    assert config.live_source_enabled is True
    assert config.live_source_url == "https://example.com/feed.xml"
    assert config.live_source_poll_interval_seconds == 120
    assert config.live_source_timeout_seconds == 9
    assert config.live_source_max_items_per_run == 25
    assert config.live_source_staleness_threshold_seconds == 3600
