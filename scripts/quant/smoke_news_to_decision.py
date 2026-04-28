from app.decision_context import build_decision_context
from app.decision_engine import evaluate_decision_context
from app.news_decision_adapter import adapt_news_for_decision


def main() -> None:
    news = adapt_news_for_decision(
        {
            "event_type": "financing",
            "headline": "Company announces registered direct offering",
            "raw_provider_extra": "ignored",
        }
    )

    context = build_decision_context(
        symbol="aapl",
        news=news,
        quant_signal={
            "price_change_pct": 12.0,
            "relative_volume": 3.0,
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
        "symbol": "AAPL",
    }

    print("news to decision smoke ok")


if __name__ == "__main__":
    main()
