
from dataclasses import dataclass

@dataclass
class DecisionContextPayload:
    decision_score: float = 0.0
    confidence: float = 0.0
    risk_flags: list = None
