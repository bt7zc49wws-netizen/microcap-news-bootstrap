from app.execution.summary import build_execution_summary
from app.execution.orders import build_execution_orders

def test_execution_summary():
    orders=[
        {"symbol":"AAPL","qty":5,"notional":1000},
        {"symbol":"TSLA","qty":2,"notional":500}
    ]
    result=build_execution_summary(orders)
    assert result["total_orders"]==2
    assert result["total_notional"]==1500
    assert result["total_qty"]==7

def test_execution_summary_empty():
    result=build_execution_summary([])
    assert result["total_orders"]==0
    assert result["total_notional"]==0
    assert result["total_qty"]==0

def test_execution_summary_zero_values():
    orders=[{"symbol":"AAPL","qty":0,"notional":0}]
    result=build_execution_summary(orders)
    assert result["total_orders"]==1
    assert result["total_notional"]==0
    assert result["total_qty"]==0

def test_execution_summary_multiple_orders():
    orders=[{"symbol":"AAPL","qty":5,"notional":1000},{"symbol":"TSLA","qty":2,"notional":500},{"symbol":"NVDA","qty":3,"notional":900}]
    result=build_execution_summary(orders)
    assert result["total_orders"]==3
    assert result["total_notional"]==2400
    assert result["total_qty"]==10

def test_execution_summary_notional_matches_orders():
    orders=build_execution_orders({"AAPL":1000,"TSLA":500},{"AAPL":200,"TSLA":250})
    result=build_execution_summary(orders)
    assert result["total_notional"]==1500
    assert result["total_orders"]==2
