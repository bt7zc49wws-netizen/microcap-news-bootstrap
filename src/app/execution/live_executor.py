from app.market.ib_stream import get_price


def execute(symbol: str, decision: dict) -> dict:
    price = get_price(symbol)

    return {
        "symbol": symbol,
        "action": decision["decision"],
        "price": price,
        "status": "paper_fill"
    }
