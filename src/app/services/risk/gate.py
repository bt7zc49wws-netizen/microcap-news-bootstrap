from app.services.risk.types import RiskCheckResult, RiskLimits

RISK_REASON_CODES = {
    "INVALID_ORDER_VALUE",
    "INVALID_DAILY_LOSS",
    "INVALID_TRADES_TODAY",
    "INVALID_RISK_LIMITS",
    "MAX_POSITION_EXCEEDED",
    "MAX_DAILY_LOSS_REACHED",
    "MAX_TRADES_REACHED",
    "RISK_CHECK_PASSED",
}


def _risk_result(*, allowed: bool, reason_code: str, reason_label: str) -> RiskCheckResult:
    if reason_code not in RISK_REASON_CODES:
        raise ValueError("risk_reason_code_unknown")
    return RiskCheckResult(
        allowed=allowed,
        reason_code=reason_code,
        reason_label=reason_label,
    )


def check_order_risk(
    *,
    order_value_usd: float,
    realized_daily_loss_usd: float,
    trades_today: int,
    limits: RiskLimits,
) -> RiskCheckResult:
    if order_value_usd <= 0:
        return _risk_result(
            allowed=False,
            reason_code="INVALID_ORDER_VALUE",
            reason_label="Invalid order value",
        )

    if realized_daily_loss_usd < 0:
        return _risk_result(
            allowed=False,
            reason_code="INVALID_DAILY_LOSS",
            reason_label="Invalid daily loss",
        )

    if trades_today < 0:
        return _risk_result(
            allowed=False,
            reason_code="INVALID_TRADES_TODAY",
            reason_label="Invalid trades today",
        )

    if (
        limits.max_position_usd <= 0
        or limits.max_daily_loss_usd <= 0
        or limits.max_trades_per_day <= 0
    ):
        return _risk_result(
            allowed=False,
            reason_code="INVALID_RISK_LIMITS",
            reason_label="Invalid risk limits",
        )

    if order_value_usd > limits.max_position_usd:
        return _risk_result(
            allowed=False,
            reason_code="MAX_POSITION_EXCEEDED",
            reason_label="Max position exceeded",
        )

    if realized_daily_loss_usd >= limits.max_daily_loss_usd:
        return _risk_result(
            allowed=False,
            reason_code="MAX_DAILY_LOSS_REACHED",
            reason_label="Max daily loss reached",
        )

    if trades_today >= limits.max_trades_per_day:
        return _risk_result(
            allowed=False,
            reason_code="MAX_TRADES_REACHED",
            reason_label="Max trades reached",
        )

    return _risk_result(
        allowed=True,
        reason_code="RISK_CHECK_PASSED",
        reason_label="Risk check passed",
    )
