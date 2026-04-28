import pytest

from app.quant import enrichment
from app.quant.enrichment import derive_previous_close


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
