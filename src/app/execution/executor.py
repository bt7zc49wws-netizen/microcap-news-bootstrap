from app.market.ib_stream import get_price


def execute_decision(state, symbol: str, decision: dict):
    if decision["decision"] == "no_trade":
        return {"status": "skipped"}

    return {
        "status": "paper_fill",
        "symbol": symbol,
        "price": get_price(symbol),
        "decision": decision["decision"],
    }
