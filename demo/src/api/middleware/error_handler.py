import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.exceptions.base import AppException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except AppException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message},
            )
        except Exception as e:
            logger.exception("Erro não tratado: %s", str(e))
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro interno do servidor"},
            )
