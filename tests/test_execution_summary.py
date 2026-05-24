from app.execution.summary import build_execution_summary

def test_execution_summary():
    orders=[
        {"symbol":"AAPL","qty":5,"notional":1000},
        {"symbol":"TSLA","qty":2,"notional":500}
    ]
    result=build_execution_summary(orders)
    assert result["total_orders"]==2
    assert result["total_notional"]==1500
    assert result["total_qty"]==7
