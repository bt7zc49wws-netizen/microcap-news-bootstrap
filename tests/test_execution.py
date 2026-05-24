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
