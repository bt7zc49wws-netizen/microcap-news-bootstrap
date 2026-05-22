def calculate_position_size(capital: float, confidence: float, risk_flags: list[str]) -> float:
    base = capital * 0.1
    penalty = 0.2 * len(risk_flags)
    size = base * confidence * (1 - min(penalty, 0.8))
    return max(0.0, size)
