from math import floor,isnan,isinf

def build_execution_orders(portfolio: dict, prices: dict) -> list[dict]:
    orders=[]
    valid_symbols=sorted([s for s in portfolio if isinstance(s,str)])
    for symbol in valid_symbols:
        allocation=portfolio[symbol]
        price=prices.get(symbol)
        if isinstance(allocation,bool) or not isinstance(allocation,(int,float)) or isnan(float(allocation)) or isinf(float(allocation)) or allocation<=0:
            continue
        if isinstance(price,bool) or not isinstance(price,(int,float)) or isnan(float(price)) or isinf(float(price)) or price<=0:
            continue
        qty=floor(allocation/price)
        if qty<=0:
            continue
        orders.append({"symbol":symbol,"qty":qty,"notional":qty*price})
    return orders
