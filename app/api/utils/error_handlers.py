import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_status import HttpStatusCode
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

    envelope = ResponseEnvelope.error(request=request,
                                      message=exc.detail or "HTTP ошибка",
                                      http_status=exc.status_code,
                                      code=AppResponseCode.BASIC_HTTP_ERROR)
    return JSONResponse(status_code=exc.status_code, content=envelope.model_dump())


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):

    method = request.method
    url = str(request.url)
    client = request.client.host if request.client else "неизвестно"
    user_agent = request.headers.get("user-agent", "неизвестно")

    try:
        body = await request.body()
        body_text = body.decode("utf-8", errors="replace")
    except Exception:
        body_text = "<unreadable>"

    errors = exc.errors()
    formatted_errors = []
    for err in errors:
        loc = err.get("loc", [])
        field = ".".join(str(x) for x in loc if isinstance(x, str))
        msg = err.get("msg", "Ошибка валидации")
        err_type = err.get("type", "-")
        formatted_errors.append(f"Поле '{field}': {msg} [{err_type}]")

    user_friendly_message = "Ошибка валидации:\n" + "\n".join(formatted_errors)

    logger.warning(
        f"[Validation error] {method} {url} from {client} ({user_agent})\n"
        f"Body: {body_text}\n"
        f"Errors:\n{user_friendly_message}\n"
        f"{traceback.format_exc()}"
    )

    envelope = ResponseEnvelope.error(
        request=request,
        message=user_friendly_message,
        http_status=HttpStatusCode.UNPROCESSABLE_ENTITY,
        code=AppResponseCode.VALIDATION_ERROR
    )
    return JSONResponse(status_code=HttpStatusCode.UNPROCESSABLE_ENTITY, content=envelope.model_dump())


async def custom_general_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Необработанное исключение: {exc}\n{traceback.format_exc()}")

    envelope = ResponseEnvelope.error(request=request,
                                      message="Внутренняя ошибка сервера – непредвиденная ошибка на стороне сервера. Требует срочного вмешательства.",
                                      http_status=HttpStatusCode.INTERNAL_SERVER_ERROR,
                                      code=AppResponseCode.CRITICAL_ERROR)
    return JSONResponse(status_code=HttpStatusCode.INTERNAL_SERVER_ERROR, content=envelope.model_dump())
