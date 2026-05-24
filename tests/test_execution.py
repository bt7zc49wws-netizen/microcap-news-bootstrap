from app.execution.orders import build_execution_orders

def test_build_execution_orders_qty_and_notional():
    portfolio = {"AAPL": 1000, "TSLA": 500}
    prices = {"AAPL": 200, "TSLA": 250}
    assert build_execution_orders(portfolio, prices) == [
        {"symbol": "AAPL", "qty": 5, "notional": 1000},
        {"symbol": "TSLA", "qty": 2, "notional": 500},
    ]

def test_build_execution_orders_deterministic_order():
    portfolio = {"TSLA": 500, "AAPL": 1000}
    prices = {"AAPL": 200, "TSLA": 250}
    assert [o["symbol"] for o in build_execution_orders(portfolio, prices)] == ["AAPL", "TSLA"]

def test_build_execution_orders_zero_price_safe():
    assert build_execution_orders({"AAPL": 1000}, {"AAPL": 0}) == []

def test_build_execution_orders_empty_safe():
    assert build_execution_orders({}, {}) == []
from app.execution.orders import build_execution_orders

def test_execution_orders_skip_insufficient_allocation():
    portfolio={"AAPL":100}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_missing_price_safe():
    portfolio={"AAPL":1000}
    prices={}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_negative_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":-200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_negative_allocation_safe():
    portfolio={"AAPL":-1000}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]
def test_execution_orders_integer_notional():
    orders=build_execution_orders({"AAPL":1050},{"AAPL":200})
    assert orders[0]["qty"]==5
    assert orders[0]["notional"]==1000

def test_execution_orders_decimal_price_floor():
    orders=build_execution_orders({"AAPL":1000},{"AAPL":333.33})
    assert orders[0]["qty"]==3
    assert round(orders[0]["notional"],2)==999.99

def test_execution_orders_deterministic_symbol_sort():
    orders=build_execution_orders({"NVDA":900,"AAPL":1000,"TSLA":500},{"AAPL":200,"TSLA":250,"NVDA":300})
    assert [o["symbol"] for o in orders]==["AAPL","NVDA","TSLA"]

def test_execution_orders_zero_qty_filtered():
    orders=build_execution_orders({"AAPL":199},{"AAPL":200})
    assert len(orders)==0

def test_execution_orders_price_precision():
    orders=build_execution_orders({"AAPL":1000},{"AAPL":199.99})
    assert orders[0]["qty"]==5
    assert round(orders[0]["notional"],2)==999.95

def test_execution_orders_exact_allocation_match():
    orders=build_execution_orders({"AAPL":1000},{"AAPL":100})
    assert orders[0]["qty"]==10
    assert orders[0]["notional"]==1000

def test_execution_orders_fractional_allocation_floor():
    orders=build_execution_orders({"AAPL":1000.75},{"AAPL":200})
    assert orders[0]["qty"]==5
    assert orders[0]["notional"]==1000

def test_execution_orders_multiple_invalid_entries():
    portfolio={"AAPL":1000,"TSLA":500,"NVDA":100}
    prices={"AAPL":200,"TSLA":0,"NVDA":300}
    orders=build_execution_orders(portfolio,prices)
    assert orders==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_large_values():
    orders=build_execution_orders({"AAPL":1000000},{"AAPL":123.45})
    assert orders[0]["qty"]==8100
    assert round(orders[0]["notional"],2)==999945.00

def test_execution_orders_multiple_valid_entries_total_notional():
    orders=build_execution_orders({"AAPL":1000,"TSLA":500,"NVDA":900},{"AAPL":200,"TSLA":250,"NVDA":300})
    assert sum(o["notional"] for o in orders)==2400
from app.execution.orders import build_execution_orders

def test_execution_orders_duplicate_determinism():
    p1={"TSLA":500,"AAPL":1000}
    p2={"AAPL":1000,"TSLA":500}
    prices={"AAPL":200,"TSLA":250}
    assert build_execution_orders(p1,prices)==build_execution_orders(p2,prices)

def test_execution_orders_missing_symbol_price_safe():
    portfolio={"AAPL":1000,"TSLA":500}
    prices={"AAPL":200}
    orders=build_execution_orders(portfolio,prices)
    assert orders==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_none_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":None}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_string_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":"200"}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_bool_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":True}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_none_allocation_safe():
    portfolio={"AAPL":None}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_bool_allocation_safe():
    portfolio={"AAPL":True}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_nan_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":float("nan")}
    assert build_execution_orders(portfolio,prices)==[]
