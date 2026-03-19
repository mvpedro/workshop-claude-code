from src.api.events import bus
from src.api.events.types import OrderCreated, OrderStatusChanged, StockLow

def setup_event_handlers() -> None:
    bus.subscribe(OrderCreated, _log_order_created)
    bus.subscribe(OrderStatusChanged, _log_status_changed)
    bus.subscribe(StockLow, _log_stock_low)

def _log_order_created(event: OrderCreated) -> None:
    import logging
    logging.getLogger(__name__).info(
        "Pedido criado: %s (cliente: %s, total: R$%.2f)",
        event.order_id, event.customer_id, event.total / 100,
    )

def _log_status_changed(event: OrderStatusChanged) -> None:
    import logging
    logging.getLogger(__name__).info(
        "Status do pedido %s alterado: %s → %s",
        event.order_id, event.old_status, event.new_status,
    )

def _log_stock_low(event: StockLow) -> None:
    import logging
    logging.getLogger(__name__).warning(
        "Estoque baixo: produto %s com %d unidades (limite: %d)",
        event.product_id, event.current_stock, event.threshold,
    )
