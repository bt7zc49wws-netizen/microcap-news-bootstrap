from datetime import UTC, datetime

import pytest

from app.services.edge.measurement import build_edge_measurement, calculate_return_pct


def test_calculate_return_pct_positive():
    assert calculate_return_pct(1.00, 1.10) == pytest.approx(10.0)


def test_calculate_return_pct_negative():
    assert calculate_return_pct(1.00, 0.90) == pytest.approx(-10.0)


def test_calculate_return_pct_rejects_zero_start_price():
    with pytest.raises(ValueError, match="start_price must be greater than zero."):
        calculate_return_pct(0, 1.00)


def test_build_edge_measurement():
    now = datetime.now(UTC)

    measurement = build_edge_measurement(
        signal_id="signal-1",
        symbol="ABCD",
        event_time=now,
        measured_at=now,
        horizon_seconds=300,
        start_price=1.00,
        end_price=1.20,
    )

    assert measurement.signal_id == "signal-1"
    assert measurement.symbol == "ABCD"
    assert measurement.horizon_seconds == 300
    assert measurement.return_pct == pytest.approx(20.0)
