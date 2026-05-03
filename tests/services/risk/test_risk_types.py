from app.services.risk.types import RiskCheckResult, RiskLimits


def test_risk_check_result_shape():
    result = RiskCheckResult(
        allowed=False,
        reason_code="MAX_POSITION_EXCEEDED",
        reason_label="Max position exceeded",
    )

    assert result.allowed is False
    assert result.reason_code == "MAX_POSITION_EXCEEDED"
    assert result.reason_label == "Max position exceeded"


def test_risk_limits_shape():
    limits = RiskLimits(
        max_position_usd=1000.0,
        max_daily_loss_usd=200.0,
        max_trades_per_day=5,
    )

    assert limits.max_position_usd == 1000.0
    assert limits.max_daily_loss_usd == 200.0
    assert limits.max_trades_per_day == 5


def test_risk_check_result_fields_are_stable():
    result = RiskCheckResult(
        allowed=False,
        reason_code="MAX_POSITION_EXCEEDED",
        reason_label="Max position exceeded",
    )

    assert tuple(result.__dataclass_fields__) == (
        "allowed",
        "reason_code",
        "reason_label",
    )


def test_risk_limits_fields_are_stable():
    limits = RiskLimits(
        max_position_usd=1000.0,
        max_daily_loss_usd=200.0,
        max_trades_per_day=5,
    )

    assert tuple(limits.__dataclass_fields__) == (
        "max_position_usd",
        "max_daily_loss_usd",
        "max_trades_per_day",
    )
