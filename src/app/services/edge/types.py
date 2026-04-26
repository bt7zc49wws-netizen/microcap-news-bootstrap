from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EdgeMeasurement:
    signal_id: str
    symbol: str
    event_time: datetime
    measured_at: datetime
    horizon_seconds: int
    start_price: float
    end_price: float
    return_pct: float
    max_favorable_excursion_pct: float | None = None
    max_adverse_excursion_pct: float | None = None
