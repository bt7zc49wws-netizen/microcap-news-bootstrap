from datetime import datetime

from app.services.edge.types import EdgeMeasurement


def calculate_return_pct(start_price: float, end_price: float) -> float:
    if start_price <= 0:
        raise ValueError("start_price must be greater than zero.")
    return ((end_price - start_price) / start_price) * 100


def build_edge_measurement(
    *,
    signal_id: str,
    symbol: str,
    event_time: datetime,
    measured_at: datetime,
    horizon_seconds: int,
    start_price: float,
    end_price: float,
) -> EdgeMeasurement:
    return EdgeMeasurement(
        signal_id=signal_id,
        symbol=symbol,
        event_time=event_time,
        measured_at=measured_at,
        horizon_seconds=horizon_seconds,
        start_price=start_price,
        end_price=end_price,
        return_pct=calculate_return_pct(start_price, end_price),
    )
