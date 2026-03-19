import logging

logger = logging.getLogger(__name__)


def process_status_change(order_id: str, old_status: str, new_status: str) -> None:
    logger.info(
        "[BACKGROUND] Processando mudança de status: pedido %s (%s → %s)",
        order_id, old_status, new_status,
    )
