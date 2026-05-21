from app.risk_flags import build_risk_flags


def test_build_risk_flags_returns_empty_for_safe_inputs() -> None:
    result = build_risk_flags(
        event_type="earnings",
        price_change=5.0,
        relative_volume=2.0,
    )

    assert result == []


def test_build_risk_flags_detects_low_relative_volume() -> None:
    result = build_risk_flags(
        event_type="earnings",
        price_change=5.0,
        relative_volume=0.5,
    )

    assert result == ["low_relative_volume"]


def test_build_risk_flags_detects_negative_price_action() -> None:
    result = build_risk_flags(
        event_type="earnings",
        price_change=-10.0,
        relative_volume=2.0,
    )

    assert result == ["negative_price_action"]


def test_build_risk_flags_detects_financing_risk() -> None:
    result = build_risk_flags(
        event_type="financing",
        price_change=10.0,
        relative_volume=2.0,
    )

    assert result == ["financing_risk"]


def test_build_risk_flags_detects_dilution_risk() -> None:
    result = build_risk_flags(
        event_type="dilution",
        price_change=10.0,
        relative_volume=2.0,
    )

    assert result == ["dilution_risk"]


def test_build_risk_flags_detects_halt_risk() -> None:
    result = build_risk_flags(
        event_type="earnings",
        price_change=30.0,
        relative_volume=2.0,
    )

    assert result == ["halt_risk"]


def test_build_risk_flags_detects_extreme_relative_volume() -> None:
    result = build_risk_flags(
        event_type="earnings",
        price_change=10.0,
        relative_volume=15.0,
    )

    assert result == ["extreme_relative_volume"]
