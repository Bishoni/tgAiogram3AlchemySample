import logging
import traceback
from functools import wraps
from typing import Callable, Awaitable, ParamSpec, TypeVar

from aiogram.exceptions import (
    TelegramAPIError, TelegramBadRequest, TelegramNotFound, TelegramForbiddenError,
    TelegramRetryAfter, TelegramServerError, TelegramUnauthorizedError,
    TelegramConflictError, TelegramEntityTooLarge, RestartingTelegram, TelegramNetworkError
)

from app.api.docs.Consts.telegram_response_data import TELEGRAM_API_ERROR_MESSAGES
from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.response import ResponseFromAnotherLogic

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R", bound=ResponseFromAnotherLogic)


def wrap_telegram_error_handler(func: Callable[P, Awaitable[ResponseFromAnotherLogic]]) -> Callable[P, Awaitable[ResponseFromAnotherLogic]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResponseFromAnotherLogic:
        user_id = kwargs.get("user_id", "unknown")

        try:
            return await func(*args, **kwargs)

        except TelegramRetryAfter as e:
            status = HttpStatusCode.TOO_MANY_REQUESTS
            msg = TELEGRAM_API_ERROR_MESSAGES[status] + f". Повторите через {e.retry_after} секунд!"
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_429)

        except TelegramNotFound:
            status = HttpStatusCode.NOT_FOUND
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_404)

        except TelegramForbiddenError:
            status = HttpStatusCode.FORBIDDEN
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_403)

        except TelegramBadRequest as e:
            if "chat not found" in str(e).lower():
                status = HttpStatusCode.NOT_FOUND
                code = AppResponseCode.TG_404
            else:
                status = HttpStatusCode.BAD_REQUEST
                code = AppResponseCode.TG_400
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=code)

        except TelegramUnauthorizedError:
            status = HttpStatusCode.UNAUTHORIZED
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_401)

        except TelegramConflictError:
            status = HttpStatusCode.CONFLICT
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_409)

        except TelegramEntityTooLarge:
            status = HttpStatusCode.PAYLOAD_TOO_LARGE
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_413)

        except RestartingTelegram:
            status = HttpStatusCode.SERVICE_UNAVAILABLE
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_503)

        except TelegramServerError:
            status = HttpStatusCode.SERVICE_UNAVAILABLE
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_503)

        except TelegramNetworkError:
            status = HttpStatusCode.GATEWAY_TIMEOUT
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_504)

        except TelegramAPIError:
            status = HttpStatusCode.INTERNAL_SERVER_ERROR
            msg = TELEGRAM_API_ERROR_MESSAGES[status]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.TG_500)

        except Exception:
            status = HttpStatusCode.INTERNAL_SERVER_ERROR
            msg = "Непредвиденная ошибка при работе с Telegram Bot API."
            logger.critical(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message=msg, http_status=status, code=AppResponseCode.SYS_500)

    return wrapper
