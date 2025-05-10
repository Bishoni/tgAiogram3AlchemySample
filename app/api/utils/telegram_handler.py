from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any, AsyncGenerator

from fastapi import status
import traceback
import logging

from aiogram.exceptions import (
    TelegramAPIError, TelegramBadRequest, TelegramNotFound, TelegramForbiddenError,
    TelegramRetryAfter, TelegramServerError, TelegramUnauthorizedError,
    TelegramConflictError, TelegramEntityTooLarge, RestartingTelegram, TelegramNetworkError
)

from app.api.docs.default_telegram_errors import TELEGRAM_API_ERROR_MESSAGES

logger = logging.getLogger(__name__)


class TelegramErrorContext(SimpleNamespace):
    result: dict = {}  # Если пусто — значит ошибки не было


@asynccontextmanager
async def telegram_api_error_handler(user_id: int = -1) -> AsyncGenerator[TelegramErrorContext, Any]:
    ctx = TelegramErrorContext()

    try:
        yield ctx
    except TelegramRetryAfter as e:
        msg = TELEGRAM_API_ERROR_MESSAGES[429] + f" Повторите через {e.retry_after} секунд."
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 429, "message": msg}

    except TelegramNotFound:
        msg = TELEGRAM_API_ERROR_MESSAGES[404]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 404, "message": msg}

    except TelegramForbiddenError:
        msg = TELEGRAM_API_ERROR_MESSAGES[403]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 403, "message": msg}

    except TelegramBadRequest as e:
        if "chat not found" in str(e).lower():
            msg = TELEGRAM_API_ERROR_MESSAGES[404]
            http_status = 404
        else:
            msg = TELEGRAM_API_ERROR_MESSAGES[400] + f" ({e})"
            http_status = 400
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": http_status, "message": msg}

    except TelegramUnauthorizedError:
        msg = TELEGRAM_API_ERROR_MESSAGES[401]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 401, "message": msg}

    except TelegramConflictError:
        msg = TELEGRAM_API_ERROR_MESSAGES[409]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 409, "message": msg}

    except TelegramEntityTooLarge:
        msg = TELEGRAM_API_ERROR_MESSAGES[413]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 413, "message": msg}

    except RestartingTelegram:
        msg = TELEGRAM_API_ERROR_MESSAGES[503]
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 503, "message": msg}

    except TelegramServerError:
        msg = TELEGRAM_API_ERROR_MESSAGES[503]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 503, "message": msg}

    except TelegramNetworkError:
        msg = TELEGRAM_API_ERROR_MESSAGES[504]
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 504, "message": msg}

    except TelegramAPIError as e:
        msg = TELEGRAM_API_ERROR_MESSAGES[500] + f": {e}"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 500, "message": msg}

    except Exception as e:
        msg = f"Непредвиденная ошибка: {e}"
        logger.critical(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        ctx.result = {"http_status": 500, "message": msg}