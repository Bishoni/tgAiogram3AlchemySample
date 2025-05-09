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

from app.api.utils.error_handlers import (
    custom_http_exception_handler,
    custom_validation_exception_handler,
    custom_general_exception_handler,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI: API_V1 запущен")
    yield
    logger.info("FastAPI: API_V1 остановлен")


api_middlewares: List[Middleware] = [
    Middleware(LoggingMiddleware)
]

app = FastAPI(
    title="Bot_API_V1",
    lifespan=lifespan,
    middleware=api_middlewares,
    docs_url="/docs" if settings.API_V1_ENABLE_DEBUG else None,
    redoc_url="/redoc" if settings.API_V1_ENABLE_DEBUG else None,
    openapi_url="/openapi.json" if settings.API_V1_ENABLE_DEBUG else None,
    log_config=None)



app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(Exception, custom_general_exception_handler)

app.include_router(api_router, prefix="/api/v1")
