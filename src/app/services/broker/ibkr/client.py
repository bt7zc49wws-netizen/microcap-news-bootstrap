from datetime import UTC, datetime

from app.services.paper_trading.types import PaperOrder


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
            submitted_at=datetime.now(UTC),
        )
