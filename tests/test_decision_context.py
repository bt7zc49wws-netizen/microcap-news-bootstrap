import pytest

from app.decision_context import build_decision_context
from app.quant.signals import QUANT_SIGNAL_FIELDS


def _quant_signal(**overrides: float) -> dict[str, float]:
    signal = {field: 1.0 for field in QUANT_SIGNAL_FIELDS}
    signal.update(overrides)
    return signal


def test_build_decision_context_combines_news_and_quant_signal() -> None:
    context = build_decision_context(
        symbol="aapl",
        news={
            "event_type": "financing",
            "headline": "Company announces registered direct offering",
        },
        quant_signal=_quant_signal(price_change_pct=12.5, relative_volume=3.2),
    )

    assert context == {
        "symbol": "AAPL",
        "news": {
            "event_type": "financing",
            "headline": "Company announces registered direct offering",
        },
        "quant_signal": {
            **_quant_signal(),
            "price_change_pct": pytest.approx(12.5),
            "relative_volume": pytest.approx(3.2),
        },
    }


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {
                "symbol": "",
                "news": {"event_type": "financing"},
                "quant_signal": _quant_signal(),
            },
            "symbol must not be empty",
        ),
        (
            {
                "symbol": "AAPL",
                "news": {},
                "quant_signal": _quant_signal(),
            },
            "news must not be empty",
        ),
        (
            {
                "symbol": "AAPL",
                "news": {"event_type": "financing"},
                "quant_signal": {},
            },
            "quant_signal must not be empty",
        ),
    ],
)
def test_build_decision_context_rejects_missing_inputs(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        build_decision_context(**kwargs)


def test_build_decision_context_can_include_audit_trace() -> None:
    context = build_decision_context(
        symbol="aapl",
        news={"event_type": "financing"},
        quant_signal=_quant_signal(price_change_pct=12.5, relative_volume=3.2),
        audit_trace={
            "market_source": "stooq",
            "news_source": "offline-smoke",
            "pipeline": "full_offline_decision",
        },
    )

    assert context == {
        "symbol": "AAPL",
        "news": {"event_type": "financing"},
        "quant_signal": {
            **_quant_signal(),
            "price_change_pct": pytest.approx(12.5),
            "relative_volume": pytest.approx(3.2),
        },
        "audit_trace": {
            "market_source": "stooq",
            "news_source": "offline-smoke",
            "pipeline": "full_offline_decision",
        },
    }


def test_build_decision_context_rejects_quant_signal_field_mismatch() -> None:
    with pytest.raises(ValueError, match="quant_signal_fields_mismatch"):
        build_decision_context(
            symbol="AAPL",
            news={"event_type": "financing"},
            quant_signal={"price_change_pct": 1.0},
        )
