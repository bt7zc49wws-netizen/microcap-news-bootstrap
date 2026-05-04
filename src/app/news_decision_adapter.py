"""Adapt news classification output into decision-context news input.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- pure validation/adaptation only
"""

from __future__ import annotations


def adapt_news_for_decision(classification: Mapping[str, object]) -> NewsDecisionInput:
    event_type = classification.get("event_type")
    headline = classification.get("headline")

    if event_type is None or not str(event_type).strip():
        raise ValueError("event_type must not be empty")
    if headline is None or not str(headline).strip():
        raise ValueError("headline must not be empty")

    return {
        "event_type": str(event_type).strip(),
        "headline": str(headline).strip(),
    }
