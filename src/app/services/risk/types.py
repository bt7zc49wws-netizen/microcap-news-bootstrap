from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskCheckResult:
    allowed: bool
    reason_code: str
    reason_label: str


@dataclass(frozen=True, slots=True)
class RiskLimits:
    max_position_usd: float
    max_daily_loss_usd: float
    max_trades_per_day: int
