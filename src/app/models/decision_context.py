"""Typed decision context payloads."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionContextPayload:
    confidence: float = 0.0
    risk_flags: list[str] = field(default_factory=list)
