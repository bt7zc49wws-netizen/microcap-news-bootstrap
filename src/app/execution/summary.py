def build_execution_summary(orders:list[dict])->dict:
    return {
        "total_orders":len(orders),
        "total_notional":sum(o["notional"] for o in orders),
        "total_qty":sum(o["qty"] for o in orders)
    }
