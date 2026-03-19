import logging

from src.api.events.types import OrderCreated, OrderStatusChanged

logger = logging.getLogger(__name__)


def handle_order_created(event: OrderCreated) -> None:
    logger.info(
        "[NOTIFICAÇÃO] Confirmação de pedido enviada para cliente %s "
        "(pedido: %s, total: R$%.2f)",
        event.customer_id, event.order_id, event.total / 100,
    )


def handle_status_changed(event: OrderStatusChanged) -> None:
    logger.info(
        "[NOTIFICAÇÃO] Atualização de status enviada para pedido %s: %s → %s",
        event.order_id, event.old_status, event.new_status,
    )
