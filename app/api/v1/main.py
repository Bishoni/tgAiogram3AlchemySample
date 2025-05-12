import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from starlette.middleware import Middleware

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.middlewares.LoggingMiddleware import LoggingMiddleware
from app.api.v1.routes import api_router
from app.config.settings import settings

from app.api.utils.error_handlers import (custom_http_exception_handler, custom_validation_exception_handler,
                                          custom_general_exception_handler)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI: API_V1 запущен")
    yield
    logger.info("FastAPI: API_V1 остановлен")


api_middlewares: List[Middleware] = [
    Middleware(LoggingMiddleware)
]

tags_metadata = [
    {
        "name": "system",
        "description": (
            "Системные методы API: проверка доступности, состояние сервиса, "
            "healthcheck и другие вспомогательные эндпоинты."
        )
    },
    {
        "name": "users",
        "description": (
            "Методы для работы с пользователями Telegram: "
            "просмотр и управление профилем, идентификация."
        )
    },
    {
        "name": "messages",
        "description": (
            "Отправка сообщений через Telegram-бота, уведомления. "
            "Используется для взаимодействия с конечными пользователями."
        )
    }
]

app = FastAPI(
    title="Sample API",
    version="1.0.0",
    description="API для Telegram-бота. Позволяет управлять пользователями, сообщениями и системными действиями.",
    summary="Бэкенд Telegram-бота",
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    middleware=api_middlewares,
    docs_url="/docs" if settings.API_V1_ENABLE_DEBUG else None,
    redoc_url="/redoc" if settings.API_V1_ENABLE_DEBUG else None,
    openapi_url="/openapi.json" if settings.API_V1_ENABLE_DEBUG else None,
    log_config=None
)



app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(Exception, custom_general_exception_handler)

app.include_router(api_router, prefix="/api/v1")
