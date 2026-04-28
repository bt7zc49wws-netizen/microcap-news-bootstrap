"""Build decision context from offline-safe news and quant inputs.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- pure composition only
"""

from __future__ import annotations


def build_decision_context(
    *,
    symbol: str,
    news: dict,
    quant_signal: dict[str, float],
) -> dict:
    """Build a decision context from already-computed news and quant inputs."""
    if not symbol:
        raise ValueError("symbol must not be empty")
    if not news:
        raise ValueError("news must not be empty")
    if not quant_signal:
        raise ValueError("quant_signal must not be empty")

    return {
        "symbol": symbol.upper(),
        "news": news,
        "quant_signal": quant_signal,
    }
