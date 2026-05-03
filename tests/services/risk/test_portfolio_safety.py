import pytest

from app.services.risk.portfolio_safety import (
    PORTFOLIO_SAFETY_REASON_CODES,
    PORTFOLIO_SAFETY_RESULT_FIELDS,
    PortfolioSafetyResult,
    check_portfolio_safety,
)


def test_portfolio_safety_allows_valid_projection() -> None:
    result = check_portfolio_safety(
        account_equity_usd=10000.0,
        available_cash_usd=7000.0,
        current_exposure_usd=2000.0,
        proposed_notional_usd=1000.0,
        max_total_exposure_fraction=0.5,
        min_cash_buffer_fraction=0.2,
    )

    assert result == PortfolioSafetyResult(
        allowed=True,
        reason_code="PORTFOLIO_CHECK_PASSED",
        reason_label="Portfolio check passed",
        projected_exposure_usd=3000.0,
        projected_exposure_fraction=0.3,
        projected_cash_usd=6000.0,
        projected_cash_buffer_fraction=0.6,
    )


def test_portfolio_safety_rejects_invalid_inputs() -> None:
    result = check_portfolio_safety(
        account_equity_usd=0.0,
        available_cash_usd=7000.0,
        current_exposure_usd=2000.0,
        proposed_notional_usd=1000.0,
        max_total_exposure_fraction=0.5,
        min_cash_buffer_fraction=0.2,
    )

    assert result.allowed is False
    assert result.reason_code == "INVALID_PORTFOLIO_INPUTS"


def test_portfolio_safety_rejects_max_exposure_exceeded() -> None:
    result = check_portfolio_safety(
        account_equity_usd=10000.0,
        available_cash_usd=7000.0,
        current_exposure_usd=4000.0,
        proposed_notional_usd=2000.0,
        max_total_exposure_fraction=0.5,
        min_cash_buffer_fraction=0.1,
    )

    assert result.allowed is False
    assert result.reason_code == "MAX_EXPOSURE_EXCEEDED"


def test_portfolio_safety_rejects_cash_buffer_breached() -> None:
    result = check_portfolio_safety(
        account_equity_usd=10000.0,
        available_cash_usd=2500.0,
        current_exposure_usd=1000.0,
        proposed_notional_usd=1000.0,
        max_total_exposure_fraction=0.5,
        min_cash_buffer_fraction=0.2,
    )

    assert result.allowed is False
    assert result.reason_code == "CASH_BUFFER_BREACHED"


def test_portfolio_safety_reason_codes_are_canonical() -> None:
    assert PORTFOLIO_SAFETY_REASON_CODES == {
        "INVALID_PORTFOLIO_INPUTS",
        "MAX_EXPOSURE_EXCEEDED",
        "CASH_BUFFER_BREACHED",
        "PORTFOLIO_CHECK_PASSED",
    }


def test_portfolio_safety_result_fields_are_stable() -> None:
    assert tuple(PortfolioSafetyResult.__dataclass_fields__) == PORTFOLIO_SAFETY_RESULT_FIELDS
