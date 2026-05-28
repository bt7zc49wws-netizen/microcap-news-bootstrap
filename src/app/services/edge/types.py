from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class EdgeMeasurement:
    signal_id: str
    symbol: str
    event_time: datetime
    measured_at: datetime
    horizon_seconds: int
    start_price: float
    end_price: float
    return_pct: float
    max_favorable_excursion_pct: Optional[float] = None
    max_adverse_excursion_pct: Optional[float] = None
