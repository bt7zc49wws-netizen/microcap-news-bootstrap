import pytest

from app.services.risk.position_sizing import POSITION_SIZE_RESULT_FIELDS, PositionSizeResult, calculate_position_size


def test_calculate_position_size_returns_expected_long_size() -> None:
    result = calculate_position_size(
        account_equity_usd=10000.0,
        risk_fraction=0.01,
        entry_price=10.0,
        stop_price=9.5,
    )

    assert result == PositionSizeResult(
        account_equity_usd=10000.0,
        risk_fraction=0.01,
        risk_amount_usd=100.0,
        entry_price=10.0,
        stop_price=9.5,
        risk_per_share=0.5,
        quantity=200,
        notional_usd=2000.0,
    )


def test_calculate_position_size_floors_fractional_quantity() -> None:
    result = calculate_position_size(
        account_equity_usd=1000.0,
        risk_fraction=0.01,
        entry_price=3.0,
        stop_price=2.2,
    )

    assert result.quantity == 12
    assert result.notional_usd == 36.0


def test_calculate_position_size_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="account_equity_must_be_positive"):
        calculate_position_size(account_equity_usd=0.0, risk_fraction=0.01, entry_price=10.0, stop_price=9.5)
    with pytest.raises(ValueError, match="risk_fraction_out_of_range"):
        calculate_position_size(account_equity_usd=1000.0, risk_fraction=0.0, entry_price=10.0, stop_price=9.5)
    with pytest.raises(ValueError, match="prices_must_be_positive"):
        calculate_position_size(account_equity_usd=1000.0, risk_fraction=0.01, entry_price=0.0, stop_price=9.5)
    with pytest.raises(ValueError, match="entry_price_must_exceed_stop_price"):
        calculate_position_size(account_equity_usd=1000.0, risk_fraction=0.01, entry_price=9.5, stop_price=9.5)


def test_position_size_result_fields_are_stable() -> None:
    assert tuple(PositionSizeResult.__dataclass_fields__) == POSITION_SIZE_RESULT_FIELDS
