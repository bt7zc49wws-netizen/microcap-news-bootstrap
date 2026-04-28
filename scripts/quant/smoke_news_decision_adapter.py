from app.news_decision_adapter import adapt_news_for_decision


def main() -> None:
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
    print("news decision adapter smoke ok")


if __name__ == "__main__":
    main()
