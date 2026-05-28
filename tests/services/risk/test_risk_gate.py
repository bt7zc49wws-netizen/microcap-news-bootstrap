from app.services.risk.gate import RISK_REASON_CODES, check_order_risk
from app.services.risk.types import RiskLimits


def make_limits() -> RiskLimits:
    return RiskLimits(
        max_position_usd=1000.0,
        max_daily_loss_usd=200.0,
        max_trades_per_day=5,
    )


def test_risk_gate_passes_valid_order():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=50.0,
        trades_today=2,
        limits=make_limits(),
    )

    assert result.allowed is True
    assert result.reason_code == "RISK_CHECK_PASSED"


def test_risk_gate_rejects_invalid_order_value():
    result = check_order_risk(
        order_value_usd=0.0,
        realized_daily_loss_usd=50.0,
        trades_today=2,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "INVALID_ORDER_VALUE"


def test_risk_gate_rejects_invalid_daily_loss():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=-1.0,
        trades_today=2,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "INVALID_DAILY_LOSS"


def test_risk_gate_rejects_invalid_trades_today():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=50.0,
        trades_today=-1,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "INVALID_TRADES_TODAY"


def test_risk_gate_rejects_invalid_risk_limits():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=50.0,
        trades_today=2,
        limits=RiskLimits(
            max_position_usd=0.0,
            max_daily_loss_usd=200.0,
            max_trades_per_day=5,
        ),
    )

    assert result.allowed is False
    assert result.reason_code == "INVALID_RISK_LIMITS"


def test_risk_gate_rejects_large_position():
    result = check_order_risk(
        order_value_usd=5000.0,
        realized_daily_loss_usd=50.0,
        trades_today=2,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "MAX_POSITION_EXCEEDED"


def test_risk_gate_rejects_daily_loss_limit():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=250.0,
        trades_today=2,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "MAX_DAILY_LOSS_REACHED"


def test_risk_gate_rejects_trade_limit():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=50.0,
        trades_today=5,
        limits=make_limits(),
    )

    assert result.allowed is False
    assert result.reason_code == "MAX_TRADES_REACHED"


def test_risk_gate_rejects_low_expectancy_quality():
    result = check_order_risk(
        order_value_usd=500.0,
        realized_daily_loss_usd=50.0,
        trades_today=2,
        expectancy_quality=0.1,
        limits=RiskLimits(
            max_position_usd=1000.0,
            max_daily_loss_usd=200.0,
            max_trades_per_day=5,
            min_expectancy_quality=0.5,
        ),
    )

    assert result.allowed is False
    assert result.reason_code == "EXPECTANCY_QUALITY_TOO_LOW"


def test_risk_reason_codes_are_canonical():
    assert RISK_REASON_CODES == {
        "INVALID_ORDER_VALUE",
        "INVALID_DAILY_LOSS",
        "INVALID_TRADES_TODAY",
        "INVALID_RISK_LIMITS",
        "MAX_POSITION_EXCEEDED",
        "MAX_DAILY_LOSS_REACHED",
        "MAX_TRADES_REACHED",
        "EXPECTANCY_QUALITY_TOO_LOW",
        "RISK_CHECK_PASSED",
    }


def test_kill_switch_default_state_is_false():
    from app.services.risk.gate import kill_switch_active
    assert kill_switch_active() is False
