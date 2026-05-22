from app.services.risk.types import RiskCheckResult, RiskLimits


def test_risk_check_result_fields_are_stable():
    result = RiskCheckResult(
        allowed=True,
        reason_code="OK",
        reason_label="Passed",
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
        "min_expectancy_quality",
    )
