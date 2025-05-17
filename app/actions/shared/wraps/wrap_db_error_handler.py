import logging
import traceback
from functools import wraps
from typing import Callable, Awaitable, ParamSpec, TypeVar

from sqlalchemy.exc import SQLAlchemyError, DBAPIError, OperationalError

from app.api.schemas.response import ResponseFromAnotherLogic
from app.api.docs.enums.http_status import HttpStatusCode
from app.api.docs.enums.app_response_codes import AppResponseCode

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R", bound=ResponseFromAnotherLogic)


def wrap_db_error_handler(func: Callable[P, Awaitable[ResponseFromAnotherLogic]]) -> Callable[P, Awaitable[ResponseFromAnotherLogic]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResponseFromAnotherLogic:
        user_id = kwargs.get("user_id", "unknown")

        try:
            return await func(*args, **kwargs)

        except OperationalError as e:
            status = HttpStatusCode.SERVICE_UNAVAILABLE
            logger.warning(f"[{user_id}] Ошибка подключения к БД: {e}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message="[Database] Ошибка соединения с базой данных. Повторите позже.",
                                            http_status=status,
                                            code=AppResponseCode.DB_503)

        except DBAPIError as e:
            status = HttpStatusCode.INTERNAL_SERVER_ERROR
            logger.error(f"[{user_id}] Ошибка DBAPI: {e}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message="[Database] Внутренняя ошибка базы данных.",
                                            http_status=status,
                                            code=AppResponseCode.DB_500)

        except SQLAlchemyError as e:
            status = HttpStatusCode.INTERNAL_SERVER_ERROR
            logger.error(f"[{user_id}] Ошибка SQLAlchemy: {e}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message="[Database] Ошибка обработки запроса к базе данных.",
                                            http_status=status,
                                            code=AppResponseCode.DB_500)

        except Exception as e:
            status = HttpStatusCode.INTERNAL_SERVER_ERROR
            logger.critical(f"[{user_id}] Непредвиденная ошибка при работе с БД: {e}\n{traceback.format_exc()}")
            return ResponseFromAnotherLogic(message="[Database] Непредвиденная ошибка на сервере.",
                                            http_status=status,
                                            code=AppResponseCode.SYS_500)

    return wrapper
