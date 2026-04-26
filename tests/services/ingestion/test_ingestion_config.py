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


def test_load_provider_config_defaults(monkeypatch):
    from app.services.ingestion.config import load_provider_config

    for key in (
        "BENZINGA_API_KEY",
        "MARKET_DATA_PROVIDER",
        "POLYGON_API_KEY",
        "TIINGO_API_KEY",
        "SEC_EDGAR_USER_AGENT",
        "FUNDAMENTALS_PROVIDER",
        "FINNHUB_API_KEY",
        "FMP_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    config = load_provider_config()

    assert config.benzinga_api_key == ""
    assert config.market_data_provider == "none"
    assert config.polygon_api_key == ""
    assert config.tiingo_api_key == ""
    assert config.sec_edgar_user_agent == ""
    assert config.fundamentals_provider == "none"
    assert config.finnhub_api_key == ""
    assert config.fmp_api_key == ""


def test_load_provider_config_from_env(monkeypatch):
    from app.services.ingestion.config import load_provider_config

    monkeypatch.setenv("BENZINGA_API_KEY", "benzinga-key")
    monkeypatch.setenv("MARKET_DATA_PROVIDER", "polygon")
    monkeypatch.setenv("POLYGON_API_KEY", "polygon-key")
    monkeypatch.setenv("TIINGO_API_KEY", "tiingo-key")
    monkeypatch.setenv("SEC_EDGAR_USER_AGENT", "test@example.com")
    monkeypatch.setenv("FUNDAMENTALS_PROVIDER", "fmp")
    monkeypatch.setenv("FINNHUB_API_KEY", "finnhub-key")
    monkeypatch.setenv("FMP_API_KEY", "fmp-key")

    config = load_provider_config()

    assert config.benzinga_api_key == "benzinga-key"
    assert config.market_data_provider == "polygon"
    assert config.polygon_api_key == "polygon-key"
    assert config.tiingo_api_key == "tiingo-key"
    assert config.sec_edgar_user_agent == "test@example.com"
    assert config.fundamentals_provider == "fmp"
    assert config.finnhub_api_key == "finnhub-key"
    assert config.fmp_api_key == "fmp-key"
