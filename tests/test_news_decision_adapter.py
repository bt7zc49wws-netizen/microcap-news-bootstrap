import pytest

from app.news_decision_adapter import adapt_news_for_decision


def test_adapt_news_for_decision_returns_canonical_news_input() -> None:
    news = adapt_news_for_decision(
        {
            "event_type": "financing",
            "headline": "Company announces registered direct offering",
            "raw_provider_extra": "ignored",
        }
    )

    assert news == {
        "event_type": "financing",
        "headline": "Company announces registered direct offering",
    }


@pytest.mark.parametrize(
    ("classification", "message"),
    [
        ({"headline": "Company announces offering"}, "event_type must not be empty"),
        ({"event_type": "financing"}, "headline must not be empty"),
    ],
)
def test_adapt_news_for_decision_rejects_missing_required_fields(classification, message) -> None:
    with pytest.raises(ValueError, match=message):
        adapt_news_for_decision(classification)
