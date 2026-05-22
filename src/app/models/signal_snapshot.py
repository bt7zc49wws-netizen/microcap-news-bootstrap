
from dataclasses import dataclass

@dataclass
class SignalSnapshot:
    symbol: str = ""
    score: float = 0.0
