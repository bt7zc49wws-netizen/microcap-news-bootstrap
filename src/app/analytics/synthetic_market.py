from __future__ import annotations

import random


def generate_return(symbol: str, score: float) -> float:
    """
    score → signal strength
    noise → market randomness
    """

    base = (score - 0.5) * 2  # [-1, +1] mapping
    noise = random.uniform(-0.5, 0.5)

    return base + noise
