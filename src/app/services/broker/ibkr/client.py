from datetime import datetime, timezone

from app.services.paper_trading.types import PaperOrder, PaperFill


class IbkrPaperClient:
    broker_name = "ibkr"

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def submit_paper_order(
        self,
        *,
        order_id: str,
        symbol: str,
        side: str,
        quantity: int,
    ) -> PaperOrder:
        if not self.enabled:
            raise RuntimeError("IBKR paper trading is disabled.")

        return PaperOrder(
            order_id=order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            submitted_at=datetime.now(timezone.utc),
        )


    def confirm_fill(
        self,
        *,
        order: PaperOrder,
        fill_price: float,
    ) -> PaperFill:
        return PaperFill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            fill_price=fill_price,
            filled_at=datetime.now(timezone.utc),
        )


    def get_open_orders(self):
        return list(self._open_orders)
