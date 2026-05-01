"""Build decision context from offline-safe news and quant inputs.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- pure composition only
"""

from __future__ import annotations

from app.quant.signals import QUANT_SIGNAL_FIELDS


def build_decision_context(
    *,
    symbol: str,
    news: dict,
    quant_signal: dict[str, float],
    audit_trace: dict | None = None,
) -> dict:
    """Build a decision context from already-computed news and quant inputs."""
    if not symbol:
        raise ValueError("symbol must not be empty")
    if not news:
        raise ValueError("news must not be empty")
    if not quant_signal:
        raise ValueError("quant_signal must not be empty")
    if set(quant_signal) != QUANT_SIGNAL_FIELDS:
        raise ValueError("quant_signal_fields_mismatch")
    if audit_trace is not None and not audit_trace:
        raise ValueError("audit_trace must not be empty")

    context = {
        "symbol": symbol.upper(),
        "news": news,
        "quant_signal": quant_signal,
    }

    if audit_trace is not None:
        context["audit_trace"] = audit_trace

    return context
