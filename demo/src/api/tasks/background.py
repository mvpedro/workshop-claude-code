import logging

logger = logging.getLogger(__name__)


def process_new_order(order_id: str) -> None:
    logger.info("[BACKGROUND] Processando novo pedido: %s", order_id)
    logger.info("[BACKGROUND] Confirmação enviada para pedido: %s", order_id)
    logger.info("[BACKGROUND] Analytics atualizados para pedido: %s", order_id)
