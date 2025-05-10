import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.api.schemas.response import ResponseEnvelope

logger = logging.getLogger(__name__)


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    method = request.method
    url = str(request.url)
    client = request.client.host if request.client else "неизвестно"
    user_agent = request.headers.get("user-agent", "неизвестно")

    logger.error(f"[HTTP {exc.status_code}] {method} {url} from {client}; user-agent: {user_agent}\n"
                 f"Detail: {exc.detail}\n"
                 f"{traceback.format_exc()}")

    envelope = ResponseEnvelope.error(request=request, message=exc.detail or "HTTP ошибка", http_status=exc.status_code)
    return JSONResponse(status_code=exc.status_code, content=envelope.model_dump())


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    method = request.method
    url = str(request.url)
    client = request.client.host if request.client else "неизвестно"
    user_agent = request.headers.get("user-agent", "неизвестно")

    try:
        body = await request.body()
    except Exception:
        body = b"<unreadable>"

    logger.warning(f"[Validation error] {method} {url} from {client} ({user_agent})\n"
                   f"Body: {body.decode('utf-8', errors='replace')}\n"
                   f"Errors: {exc.errors()}\n"
                   f"{traceback.format_exc()}")

    # todo: писать, какая именно ошибка валидации. какие неожиданные символы может в каком параметры возникли
    envelope = ResponseEnvelope.error(request=request, message="Ошибка валидации", http_status=422)
    return JSONResponse(status_code=422, content=envelope.model_dump())


async def custom_general_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Необработанное исключение: {exc}\n{traceback.format_exc()}")

    envelope = ResponseEnvelope.error(request=request, message="Внутренняя ошибка сервера – непредвиденная ошибка на стороне сервера", http_status=500)
    return JSONResponse(status_code=500, content=envelope.model_dump())
