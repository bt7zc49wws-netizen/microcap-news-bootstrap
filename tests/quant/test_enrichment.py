import pytest

from app.quant import enrichment
from app.quant.enrichment import derive_average_volume, derive_previous_close


def test_enrichment_module_imports() -> None:
    assert enrichment is not None


def test_derive_previous_close_from_second_to_last_row() -> None:
    rows = [
        {"close": 9.5},
        {"close": 10.0},
        {"close": 12.0},
    ]

    assert derive_previous_close(rows) == pytest.approx(10.0)


def test_derive_previous_close_rejects_too_few_rows() -> None:
    with pytest.raises(ValueError, match="at least two rows"):
        derive_previous_close([{"close": 12.0}])


def test_derive_previous_close_rejects_non_numeric_close() -> None:
    with pytest.raises(ValueError, match="previous close must be numeric"):
        derive_previous_close([{"close": "10.0"}, {"close": 12.0}])


def test_derive_average_volume_uses_completed_rows_before_current() -> None:
    rows = [
        {"volume": 100.0},
        {"volume": 200.0},
        {"volume": 300.0},
        {"volume": 999.0},
    ]

    assert derive_average_volume(rows, lookback=3) == pytest.approx(200.0)


def test_derive_average_volume_uses_available_completed_rows_when_lookback_is_larger() -> None:
    rows = [
        {"volume": 100.0},
        {"volume": 200.0},
        {"volume": 999.0},
    ]

    assert derive_average_volume(rows, lookback=20) == pytest.approx(150.0)


def test_derive_average_volume_rejects_invalid_lookback() -> None:
    with pytest.raises(ValueError, match="lookback must be positive"):
        derive_average_volume([{"volume": 100.0}, {"volume": 200.0}], lookback=0)


def test_derive_average_volume_rejects_non_numeric_volume() -> None:
    with pytest.raises(ValueError, match="volume must be numeric"):
        derive_average_volume([{"volume": "100"}, {"volume": 200.0}], lookback=2)
