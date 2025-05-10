import logging
import traceback
from functools import wraps
from typing import Callable, Awaitable, ParamSpec, TypeVar

from aiogram.exceptions import (TelegramAPIError, TelegramBadRequest, TelegramNotFound, TelegramForbiddenError,
                                TelegramRetryAfter, TelegramServerError, TelegramUnauthorizedError,
                                TelegramConflictError, TelegramEntityTooLarge, RestartingTelegram, TelegramNetworkError)
from app.api.docs.default_telegram_errors import TELEGRAM_API_ERROR_MESSAGES
from app.api.schemas.response import ResponseFromTelegramLogic

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R", bound=ResponseFromTelegramLogic)


def wrap_telegram_error_handler(
    func: Callable[P, Awaitable[ResponseFromTelegramLogic]]
) -> Callable[P, Awaitable[ResponseFromTelegramLogic]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResponseFromTelegramLogic:
        user_id = kwargs.get("user_id", "unknown")

        try:
            return await func(*args, **kwargs)

        except TelegramRetryAfter as e:
            msg = TELEGRAM_API_ERROR_MESSAGES[429] + f" Повторите через {e.retry_after} секунд."
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=429)

        except TelegramNotFound:
            msg = TELEGRAM_API_ERROR_MESSAGES[404]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=404)

        except TelegramForbiddenError:
            msg = TELEGRAM_API_ERROR_MESSAGES[403]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=403)

        except TelegramBadRequest as e:
            if "chat not found" in str(e).lower():
                msg = TELEGRAM_API_ERROR_MESSAGES[404]
                http_status = 404
            else:
                msg = TELEGRAM_API_ERROR_MESSAGES[400] + f" ({e})"
                http_status = 400
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=http_status)

        except TelegramUnauthorizedError:
            msg = TELEGRAM_API_ERROR_MESSAGES[401]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=401)

        except TelegramConflictError:
            msg = TELEGRAM_API_ERROR_MESSAGES[409]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=409)

        except TelegramEntityTooLarge:
            msg = TELEGRAM_API_ERROR_MESSAGES[413]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=413)

        except RestartingTelegram:
            msg = TELEGRAM_API_ERROR_MESSAGES[503]
            logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=503)

        except TelegramServerError:
            msg = TELEGRAM_API_ERROR_MESSAGES[503]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=503)

        except TelegramNetworkError:
            msg = TELEGRAM_API_ERROR_MESSAGES[504]
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=504)

        except TelegramAPIError as e:
            msg = TELEGRAM_API_ERROR_MESSAGES[500] + f": {e}"
            logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=500)

        except Exception as e:
            msg = f"Непредвиденная ошибка: {e}"
            logger.critical(f"[{user_id}] {msg}\n{traceback.format_exc()}")
            return ResponseFromTelegramLogic(message=msg, http_status=500)

    return wrapper
