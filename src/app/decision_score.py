"""Decision score helpers."""

from __future__ import annotations


def compute_decision_score(
    *,
    confidence: float,
    risk_flag_count: int,
) -> float:
    penalty = min(risk_flag_count * 0.1, 0.5)
    score = confidence - penalty
    return max(0.0, min(score, 1.0))
