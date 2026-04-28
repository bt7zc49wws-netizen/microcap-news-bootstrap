"""Adapt news classification output into decision-context news input.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- pure validation/adaptation only
"""

from __future__ import annotations


def adapt_news_for_decision(classification: dict) -> dict:
    """Adapt classification output into decision-context news input."""
    event_type = classification.get("event_type")
    headline = classification.get("headline")

    if not event_type:
        raise ValueError("event_type must not be empty")
    if not headline:
        raise ValueError("headline must not be empty")

    return {
        "event_type": str(event_type),
        "headline": str(headline),
    }
