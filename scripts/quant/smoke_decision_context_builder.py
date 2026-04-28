from app.decision_context import build_decision_context


def main() -> None:
    context = build_decision_context(
        symbol="aapl",
        news={
            "event_type": "financing",
            "headline": "Company announces registered direct offering",
        },
        quant_signal={
            "price_change_pct": 12.5,
            "relative_volume": 3.2,
        },
    )

    assert context["symbol"] == "AAPL"
    assert context["news"]["event_type"] == "financing"
    assert context["quant_signal"]["relative_volume"] == 3.2
    print("decision context builder smoke ok")


if __name__ == "__main__":
    main()
