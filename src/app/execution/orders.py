from math import floor,isnan

def build_execution_orders(portfolio: dict, prices: dict) -> list[dict]:
    orders=[]
    for symbol in sorted(portfolio):
        allocation=portfolio[symbol]
        price=prices.get(symbol)
        if isinstance(allocation,bool) or not isinstance(allocation,(int,float)) or isnan(float(allocation)) or allocation<=0:
            continue
        if isinstance(price,bool) or not isinstance(price,(int,float)) or isnan(float(price)) or price<=0:
            continue
        qty=floor(allocation/price)
        if qty<=0:
            continue
        orders.append({"symbol":symbol,"qty":qty,"notional":qty*price})
    return orders
