from src.api.exceptions.base import AppException

class InsufficientStock(AppException):
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(
            f"Estoque insuficiente para produto {product_id}: solicitado {requested}, disponível {available}",
            status_code=409,
        )

class InvalidStatusTransition(AppException):
    def __init__(self, order_id: str, current: str, target: str):
        super().__init__(f"Transição inválida para pedido {order_id}: {current} → {target}", status_code=422)

class DuplicateEmail(AppException):
    def __init__(self, email: str):
        super().__init__(f"Email já cadastrado: {email}", status_code=409)

class NotFound(AppException):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(f"{entity} não encontrado: {entity_id}", status_code=404)
