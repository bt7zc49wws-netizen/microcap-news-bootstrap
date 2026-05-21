"""Risk flag evaluation helpers."""

from __future__ import annotations


def build_risk_flags(
    *,
    event_type: str | None,
    price_change: float,
    relative_volume: float,
) -> list[str]:
    risk_flags: list[str] = []

    if relative_volume < 1.0:
        risk_flags.append("low_relative_volume")

    if price_change < 0:
        risk_flags.append("negative_price_action")

    if event_type in {"offering", "dilution"}:
        risk_flags.append("dilution_risk")

    if event_type == "financing":
        risk_flags.append("financing_risk")

    if abs(price_change) >= 25:
        risk_flags.append("halt_risk")

    if relative_volume >= 10:
        risk_flags.append("extreme_relative_volume")

    return sorted(set(risk_flags))
