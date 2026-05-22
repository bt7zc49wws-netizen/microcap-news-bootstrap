from __future__ import annotations


def risk_gate(decision: dict, confidence: float) -> bool:
    if decision["decision"] == "no_trade":
        return False

    if confidence < 0.2:
        return False

    if len(decision["decision_context"]["risk_flags"]) >= 3:
        return False

    return True
