from app.market.ib_stream import get_last_price

def execute_decision(symbol: str, decision: str) -> dict:
    price = get_last_price(symbol)

    if decision == "no_trade":
        return {"status": "skipped", "symbol": symbol}

    return {"status": "paper_order", "symbol": symbol, "price": price}
