
from dataclasses import dataclass

@dataclass
class Decision:
    decision: str = "no_trade"
    score: float = 0.0
