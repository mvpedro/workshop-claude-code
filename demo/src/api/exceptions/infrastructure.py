from src.api.exceptions.base import AppException

class DatabaseError(AppException):
    def __init__(self, detail: str = "Erro interno no banco de dados"):
        super().__init__(detail, status_code=500)

class ExternalServiceError(AppException):
    def __init__(self, service: str, detail: str = ""):
        super().__init__(f"Erro no serviço externo '{service}': {detail}", status_code=502)
