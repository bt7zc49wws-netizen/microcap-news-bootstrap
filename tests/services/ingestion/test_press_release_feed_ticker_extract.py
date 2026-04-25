from app.services.ingestion.adapters.press_release_feed import extract_primary_ticker


def test_extract_primary_ticker_from_exchange_prefix():
    assert extract_primary_ticker(
        "Company Announces Financing",
        "Common stock trades on NASDAQ: ABCD.",
    ) == "ABCD"


def test_extract_primary_ticker_returns_none_when_missing():
    assert extract_primary_ticker("Company Announces Financing", "No ticker here.") is None


def test_extract_primary_ticker_from_headline_suffix():
    assert extract_primary_ticker(
        "Investigation Alert - IRON",
        "Body text.",
    ) == "IRON"
