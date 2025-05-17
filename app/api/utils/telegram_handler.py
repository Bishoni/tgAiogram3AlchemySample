from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any, AsyncGenerator

import traceback
import logging

from aiogram.exceptions import (
    TelegramAPIError, TelegramBadRequest, TelegramNotFound, TelegramForbiddenError,
    TelegramRetryAfter, TelegramServerError, TelegramUnauthorizedError,
    TelegramConflictError, TelegramEntityTooLarge, RestartingTelegram, TelegramNetworkError
)

from app.api.docs.consts.telegram_response_data import TELEGRAM_API_ERROR_MESSAGES
from app.api.docs.enums.http_status import HttpStatusCode

logger = logging.getLogger(__name__)


class TelegramErrorContext(SimpleNamespace):
    result: dict = {}


@asynccontextmanager
async def telegram_api_error_handler(user_id: int = -1) -> AsyncGenerator[TelegramErrorContext, Any]:
    ctx = TelegramErrorContext()

    try:
        yield ctx

    except TelegramRetryAfter as e:
        status = HttpStatusCode.TOO_MANY_REQUESTS
        msg = TELEGRAM_API_ERROR_MESSAGES[status] + f" Повторите через {e.retry_after} секунд."
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramNotFound:
        status = HttpStatusCode.NOT_FOUND
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramForbiddenError:
        status = HttpStatusCode.FORBIDDEN
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramBadRequest as e:
        if "chat not found" in str(e).lower():
            status = HttpStatusCode.NOT_FOUND
        else:
            status = HttpStatusCode.BAD_REQUEST
        msg = TELEGRAM_API_ERROR_MESSAGES[status] + f" ({e})"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramUnauthorizedError:
        status = HttpStatusCode.UNAUTHORIZED
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramConflictError:
        status = HttpStatusCode.CONFLICT
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramEntityTooLarge:
        status = HttpStatusCode.PAYLOAD_TOO_LARGE
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except RestartingTelegram:
        status = HttpStatusCode.SERVICE_UNAVAILABLE
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramServerError:
        status = HttpStatusCode.SERVICE_UNAVAILABLE
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramNetworkError:
        status = HttpStatusCode.GATEWAY_TIMEOUT
        msg = TELEGRAM_API_ERROR_MESSAGES[status]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except TelegramAPIError as e:
        status = HttpStatusCode.INTERNAL_SERVER_ERROR
        msg = TELEGRAM_API_ERROR_MESSAGES[status] + f": {e}"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except Exception as e:
        status = HttpStatusCode.INTERNAL_SERVER_ERROR
        msg = f"Непредвиденная ошибка: {e}"
        logger.critical(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}
