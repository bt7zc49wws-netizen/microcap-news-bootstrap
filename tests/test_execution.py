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

def test_execution_orders_nan_allocation_safe():
    portfolio={"AAPL":float("nan")}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_inf_price_safe():
    portfolio={"AAPL":1000}
    prices={"AAPL":float("inf")}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_inf_allocation_safe():
    portfolio={"AAPL":float("inf")}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_nan_and_inf_mix_safe():
    portfolio={"AAPL":float("nan"),"TSLA":float("inf"),"NVDA":1000}
    prices={"AAPL":200,"TSLA":250,"NVDA":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"NVDA","qty":5,"notional":1000}]

def test_execution_orders_negative_inf_safe():
    portfolio={"AAPL":float("-inf")}
    prices={"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[]

def test_execution_orders_none_symbol_safe():
    portfolio={None:1000,"AAPL":1000}
    prices={"AAPL":200,None:100}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_empty_symbol_safe():
    portfolio={"":1000,"AAPL":1000}
    prices={"":100,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_whitespace_symbol_safe():
    portfolio={"   ":1000,"AAPL":1000}
    prices={"   ":100,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_lowercase_symbol_preserved():
    portfolio={"aapl":1000}
    prices={"aapl":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"aapl","qty":5,"notional":1000}]

def test_execution_orders_case_sensitive_symbols():
    portfolio={"AAPL":1000,"aapl":1000}
    prices={"AAPL":200,"aapl":250}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000},{"symbol":"aapl","qty":4,"notional":1000}]

def test_execution_orders_unicode_symbol_preserved():
    portfolio={"ŞİRKET":1000}
    prices={"ŞİRKET":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"ŞİRKET","qty":5,"notional":1000}]

def test_execution_orders_symbol_with_spaces_preserved():
    portfolio={" AAPL ":1000}
    prices={" AAPL ":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":" AAPL ","qty":5,"notional":1000}]

def test_execution_orders_tab_symbol_safe():
    portfolio={"\t":1000,"AAPL":1000}
    prices={"\t":100,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_newline_symbol_safe():
    portfolio={"\n":1000,"AAPL":1000}
    prices={"\n":100,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_leading_trailing_spaces_distinct():
    portfolio={"AAPL":1000," AAPL ":1000}
    prices={"AAPL":200," AAPL ":250}
    assert build_execution_orders(portfolio,prices)==[{"symbol":" AAPL ","qty":4,"notional":1000},{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_symbol_sort_stability():
    portfolio={"ZZZ":1000,"AAA":1000,"MMM":1000}
    prices={"ZZZ":200,"AAA":200,"MMM":200}
    orders=build_execution_orders(portfolio,prices)
    assert [o["symbol"] for o in orders]==["AAA","MMM","ZZZ"]

def test_execution_orders_numeric_symbol_safe():
    portfolio={123:1000,"AAPL":1000}
    prices={123:200,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_tuple_symbol_safe():
    portfolio={("AAPL",):1000,"AAPL":1000}
    prices={("AAPL",):200,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000}]

def test_execution_orders_list_symbol_safe():
    portfolio={str(["AAPL"]):1000,"AAPL":1000}
    prices={str(["AAPL"]):200,"AAPL":200}
    assert build_execution_orders(portfolio,prices)==[{"symbol":"AAPL","qty":5,"notional":1000},{"symbol":"['AAPL']","qty":5,"notional":1000}]

def test_execution_orders_very_small_price():
    orders=build_execution_orders({"AAPL":1000},{"AAPL":0.01})
    assert orders[0]["qty"]==100000
    assert orders[0]["notional"]==1000

def test_execution_orders_zero_allocation_safe():
    orders=build_execution_orders({"AAPL":0},{"AAPL":200})
    assert orders==[]

def test_execution_orders_extremely_large_price_safe():
    orders=build_execution_orders({"AAPL":1000},{"AAPL":1e12})
    assert orders==[]
