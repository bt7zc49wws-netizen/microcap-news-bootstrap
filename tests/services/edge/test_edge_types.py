from datetime import UTC, datetime

from app.services.edge.types import EdgeMeasurement


def test_edge_measurement_shape():
    now = datetime.now(UTC)

    measurement = EdgeMeasurement(
        signal_id="signal-1",
        symbol="ABCD",
        event_time=now,
        measured_at=now,
        horizon_seconds=300,
        start_price=1.00,
        end_price=1.10,
        return_pct=10.0,
        max_favorable_excursion_pct=12.0,
        max_adverse_excursion_pct=-3.0,
    )

    assert measurement.signal_id == "signal-1"
    assert measurement.symbol == "ABCD"
    assert measurement.horizon_seconds == 300
    assert measurement.return_pct == 10.0
