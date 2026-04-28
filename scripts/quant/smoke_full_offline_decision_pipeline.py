from datetime import UTC, datetime

from app.classification.rules import classify_record
from app.decision_context import build_decision_context
from app.decision_engine import evaluate_decision_context
from app.models.ingestion_record import IngestionRecord
from app.news_decision_adapter import adapt_news_for_decision
from app.quant.adapters import adapt_stooq_market_snapshot
from app.quant.enrichment import enrich_stooq_market_payload
from app.quant.signals import build_quant_signal_from_snapshot
from app.services.providers.market_data.client import normalize_stooq_ohlcv_rows


def main() -> None:
    symbol = "HTCO"

    stooq_raw_rows = [
        {
            "Date": "2026-04-23",
            "Open": "0.98",
            "High": "1.02",
            "Low": "0.95",
            "Close": "1.00",
            "Volume": "90000",
        },
        {
            "Date": "2026-04-24",
            "Open": "1.00",
            "High": "1.05",
            "Low": "0.98",
            "Close": "1.00",
            "Volume": "100000",
        },
        {
            "Date": "2026-04-27",
            "Open": "1.00",
            "High": "1.25",
            "Low": "0.99",
            "Close": "1.20",
            "Volume": "350000",
        },
    ]

    rows = normalize_stooq_ohlcv_rows(stooq_raw_rows)
    enriched_payload = enrich_stooq_market_payload(
        rows,
        average_volume_lookback=2,
        vwap_lookback=2,
        atr_lookback=2,
        breakout_lookback=2,
    )
    market_snapshot = adapt_stooq_market_snapshot(enriched_payload)
    quant_signal = build_quant_signal_from_snapshot(market_snapshot)

    published_at = datetime(2026, 4, 27, 13, 30, tzinfo=UTC)
    news_record = IngestionRecord(
        record_id="offline-smoke-record",
        external_id="offline-smoke-external",
        source_name="offline-smoke",
        source_type="mock",
        symbol=symbol,
        headline="HTCO announces registered direct offering with institutional investors",
        source_event_time=published_at,
        published_at=published_at,
        ingested_at=published_at,
        processed_at=published_at,
        status="accepted",
        quality_flags="[]",
        is_duplicate=False,
    )

    classification = classify_record(news_record)
    news_signal = adapt_news_for_decision(
        {
            **classification,
            "event_type": classification["event_family"],
            "headline": news_record.headline,
        }
    )
    context = build_decision_context(
        symbol=symbol,
        news=news_signal,
        quant_signal=quant_signal,
        audit_trace={
            "market_source": "stooq",
            "news_source": "offline-smoke",
            "pipeline": "full_offline_decision",
        },
    )
    result = evaluate_decision_context(context)

    assert result == {
        "decision": "actionable",
        "reason_codes": [
            "SUPPORTED_NEWS_EVENT",
            "PRICE_CHANGE_STRONG",
            "RELATIVE_VOLUME_STRONG",
        ],
        "symbol": symbol,
    }
    assert news_signal["event_type"] in {"financing", "dilution", "offering"}
    assert quant_signal["price_change_pct"] >= 10.0
    assert quant_signal["relative_volume"] >= 2.0

    print("full offline decision pipeline smoke ok")


if __name__ == "__main__":
    main()
