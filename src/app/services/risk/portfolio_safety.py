from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioSafetyResult:
    allowed: bool
    reason_code: str
    reason_label: str
    projected_exposure_usd: float
    projected_exposure_fraction: float
    projected_cash_usd: float
    projected_cash_buffer_fraction: float


PORTFOLIO_SAFETY_RESULT_FIELDS = (
    "allowed",
    "reason_code",
    "reason_label",
    "projected_exposure_usd",
    "projected_exposure_fraction",
    "projected_cash_usd",
    "projected_cash_buffer_fraction",
)


PORTFOLIO_SAFETY_REASON_CODES = {
    "INVALID_PORTFOLIO_INPUTS",
    "MAX_EXPOSURE_EXCEEDED",
    "CASH_BUFFER_BREACHED",
    "PORTFOLIO_CHECK_PASSED",
}


def _portfolio_result(
    *,
    allowed: bool,
    reason_code: str,
    reason_label: str,
    projected_exposure_usd: float,
    projected_exposure_fraction: float,
    projected_cash_usd: float,
    projected_cash_buffer_fraction: float,
) -> PortfolioSafetyResult:
    if reason_code not in PORTFOLIO_SAFETY_REASON_CODES:
        raise ValueError("portfolio_safety_reason_code_unknown")
    return PortfolioSafetyResult(
        allowed=allowed,
        reason_code=reason_code,
        reason_label=reason_label,
        projected_exposure_usd=projected_exposure_usd,
        projected_exposure_fraction=projected_exposure_fraction,
        projected_cash_usd=projected_cash_usd,
        projected_cash_buffer_fraction=projected_cash_buffer_fraction,
    )


def check_portfolio_safety(
    *,
    account_equity_usd: float,
    available_cash_usd: float,
    current_exposure_usd: float,
    proposed_notional_usd: float,
    max_total_exposure_fraction: float,
    min_cash_buffer_fraction: float,
) -> PortfolioSafetyResult:
    projected_exposure_usd = current_exposure_usd + proposed_notional_usd
    projected_cash_usd = available_cash_usd - proposed_notional_usd
    projected_exposure_fraction = (
        projected_exposure_usd / account_equity_usd if account_equity_usd > 0 else 0.0
    )
    projected_cash_buffer_fraction = (
        projected_cash_usd / account_equity_usd if account_equity_usd > 0 else 0.0
    )

    if (
        account_equity_usd <= 0
        or available_cash_usd < 0
        or current_exposure_usd < 0
        or proposed_notional_usd <= 0
        or max_total_exposure_fraction <= 0
        or max_total_exposure_fraction > 1
        or min_cash_buffer_fraction < 0
        or min_cash_buffer_fraction >= 1
    ):
        return _portfolio_result(
            allowed=False,
            reason_code="INVALID_PORTFOLIO_INPUTS",
            reason_label="Invalid portfolio inputs",
            projected_exposure_usd=projected_exposure_usd,
            projected_exposure_fraction=projected_exposure_fraction,
            projected_cash_usd=projected_cash_usd,
            projected_cash_buffer_fraction=projected_cash_buffer_fraction,
        )

    if projected_exposure_fraction > max_total_exposure_fraction:
        return _portfolio_result(
            allowed=False,
            reason_code="MAX_EXPOSURE_EXCEEDED",
            reason_label="Max exposure exceeded",
            projected_exposure_usd=projected_exposure_usd,
            projected_exposure_fraction=projected_exposure_fraction,
            projected_cash_usd=projected_cash_usd,
            projected_cash_buffer_fraction=projected_cash_buffer_fraction,
        )

    if projected_cash_buffer_fraction < min_cash_buffer_fraction:
        return _portfolio_result(
            allowed=False,
            reason_code="CASH_BUFFER_BREACHED",
            reason_label="Cash buffer breached",
            projected_exposure_usd=projected_exposure_usd,
            projected_exposure_fraction=projected_exposure_fraction,
            projected_cash_usd=projected_cash_usd,
            projected_cash_buffer_fraction=projected_cash_buffer_fraction,
        )

    return _portfolio_result(
        allowed=True,
        reason_code="PORTFOLIO_CHECK_PASSED",
        reason_label="Portfolio check passed",
        projected_exposure_usd=projected_exposure_usd,
        projected_exposure_fraction=projected_exposure_fraction,
        projected_cash_usd=projected_cash_usd,
        projected_cash_buffer_fraction=projected_cash_buffer_fraction,
    )
