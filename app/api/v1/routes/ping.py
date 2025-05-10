import logging
import traceback

from aiogram import Bot
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.api.deps import get_session_without_commit, get_bot
from app.api.docs.default_telegram_errors import TELEGRAM_API_ERROR_RESPONSES
from app.api.schemas.response import ResponseEnvelope
from app.api.docs.common_responses import common_responses
from app.api.schemas.response import (ResponseModelSuccessExample, ErrorResponseBlockExample,
                                      ResponseConfig)
from app.api.utils.telegram_handler import telegram_api_error_handler
from app.main_dao.models import TgUser

logger = logging.getLogger(__name__)
router = APIRouter()


class PingResponseData(BaseModel):
    pong: bool = Field(..., description="Флаг, подтверждающий доступность сервиса")
    database_user_count: int = Field(...,
                                     description="Общее количество пользователей в таблице телеграмм-пользователей")
    bot_first_name: str = Field(..., description="Название Telegram-бота.")

    @staticmethod
    def example() -> dict:
        return PingResponseData(pong=True, database_user_count=12345, bot_first_name="Мой Telegram Bot").model_dump()


PING_RESPONSES_DOCS = ResponseConfig(
    success={
        200: ResponseModelSuccessExample(
            message="API функционирует корректно. Подключение к базе данных успешно. Телеграмм бот доступен.",
            description="Сервис доступен, способен выполнять SQL-запросы к БД, подключение к Telegram Bot установлено",
            data=PingResponseData.example()
        )
    },
    error=ErrorResponseBlockExample(
        errors=TELEGRAM_API_ERROR_RESPONSES
    )
)


@router.post("/ping",
            response_model=ResponseEnvelope,
            responses=common_responses(path_suffix="/ping", api_version="v1", response_config=PING_RESPONSES_DOCS),
            summary="Проверка доступности API",
            description=("Эндпоинт предназначен для проверки доступности и базовой работоспособности API-сервиса. "
                         "Возвращает флаг доступности, количество пользователей в базе данных и название Telegram Bot. "
                         "Может использоваться как healthcheck для мониторинга."),
            operation_id="pingSystemHealthCheck")
async def ping(request: Request,
               session: AsyncSession = Depends(get_session_without_commit)) -> JSONResponse:
    try:
        result = await session.execute(select(func.count()).select_from(TgUser))
        user_count = result.scalar_one()
    except Exception as e:
        logger.error(f'Ошибка пинга к БД: {e} \n{traceback.format_exc()}')
        return_content = ResponseEnvelope.error(
            request=request,
            message="Не удалось выполнить базовый SQL-запрос: возможно, база данных недоступна.",
            http_status=503)
        return JSONResponse(status_code=503, content=return_content.model_dump())

    async with telegram_api_error_handler() as ctx:
        bot: Bot = get_bot()
        bot_me = await bot.get_me()

    if "http_status" in ctx.result:
        return JSONResponse(status_code=ctx.result["http_status"],
                            content=ResponseEnvelope.error(
                                request=request,
                                message=ctx.result["message"],
                                http_status=ctx.result["http_status"]).model_dump())

    return_data = PingResponseData(pong=True, database_user_count=user_count, bot_first_name=bot_me.first_name)
    return_content = ResponseEnvelope.success(
        request=request,
        data=return_data.model_dump(),
        message="API функционирует корректно. Подключение к базе данных успешно. Телеграмм бот доступен.")
    return JSONResponse(status_code=200, content=return_content.model_dump())
