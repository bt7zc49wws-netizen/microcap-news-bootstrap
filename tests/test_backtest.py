from app.backtest.backtest_engine import run_backtest


def test_backtest_runs() -> None:
    result = run_backtest("AAPL")

    assert "pnl" in result
    assert "symbol" in result
