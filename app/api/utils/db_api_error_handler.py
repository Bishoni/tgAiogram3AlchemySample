from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any, AsyncGenerator

import logging
import traceback

from sqlalchemy.exc import SQLAlchemyError, DBAPIError, OperationalError

from app.api.docs.enums.http_status import HttpStatusCode

logger = logging.getLogger(__name__)


class DBErrorContext(SimpleNamespace):
    result: dict = {}


@asynccontextmanager
async def db_api_error_handler(user_id: int = -1) -> AsyncGenerator[DBErrorContext, Any]:
    ctx = DBErrorContext()

    try:
        yield ctx

    except OperationalError as e:
        status = HttpStatusCode.SERVICE_UNAVAILABLE
        msg = "Ошибка соединения с базой данных. Повторите попытку позже."
        logger.warning(f"[{user_id}] [DB:OperationalError] {e}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except DBAPIError as e:
        status = HttpStatusCode.INTERNAL_SERVER_ERROR
        msg = "Ошибка на уровне драйвера базы данных."
        logger.error(f"[{user_id}] [DB:DBAPIError] {e}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except SQLAlchemyError as e:
        status = HttpStatusCode.INTERNAL_SERVER_ERROR
        msg = "Ошибка при выполнении запроса к базе данных."
        logger.error(f"[{user_id}] [DB:SQLAlchemyError] {e}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}

    except Exception as e:
        status = HttpStatusCode.INTERNAL_SERVER_ERROR
        msg = "Непредвиденная ошибка при работе с базой данных."
        logger.critical(f"[{user_id}] [DB:UnexpectedError] {e}\n{traceback.format_exc()}")
        ctx.result = {"http_status": status, "message": msg}
