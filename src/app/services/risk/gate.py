from app.services.risk.types import RiskCheckResult, RiskLimits


def check_order_risk(
    *,
    order_value_usd: float,
    realized_daily_loss_usd: float,
    trades_today: int,
    limits: RiskLimits,
) -> RiskCheckResult:
    if order_value_usd <= 0:
        return RiskCheckResult(
            allowed=False,
            reason_code="INVALID_ORDER_VALUE",
            reason_label="Invalid order value",
        )

    if realized_daily_loss_usd < 0:
        return RiskCheckResult(
            allowed=False,
            reason_code="INVALID_DAILY_LOSS",
            reason_label="Invalid daily loss",
        )

    if trades_today < 0:
        return RiskCheckResult(
            allowed=False,
            reason_code="INVALID_TRADES_TODAY",
            reason_label="Invalid trades today",
        )

    if (
        limits.max_position_usd <= 0
        or limits.max_daily_loss_usd <= 0
        or limits.max_trades_per_day <= 0
    ):
        return RiskCheckResult(
            allowed=False,
            reason_code="INVALID_RISK_LIMITS",
            reason_label="Invalid risk limits",
        )

    if order_value_usd > limits.max_position_usd:
        return RiskCheckResult(
            allowed=False,
            reason_code="MAX_POSITION_EXCEEDED",
            reason_label="Max position exceeded",
        )

    if realized_daily_loss_usd >= limits.max_daily_loss_usd:
        return RiskCheckResult(
            allowed=False,
            reason_code="MAX_DAILY_LOSS_REACHED",
            reason_label="Max daily loss reached",
        )

    if trades_today >= limits.max_trades_per_day:
        return RiskCheckResult(
            allowed=False,
            reason_code="MAX_TRADES_REACHED",
            reason_label="Max trades reached",
        )

    return RiskCheckResult(
        allowed=True,
        reason_code="RISK_CHECK_PASSED",
        reason_label="Risk check passed",
    )
