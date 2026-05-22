from app.backtest.pnl_engine import simulate_trade
from app.analytics.market_data import get_price_series

def run_backtest(symbol: str) -> dict:
    prices = get_price_series(symbol)

    pnl = 0.0
    for i in range(len(prices) - 1):
        pnl += simulate_trade(prices[i], prices[i + 1])

    return {"symbol": symbol, "pnl": pnl, "trades": len(prices) - 1}
