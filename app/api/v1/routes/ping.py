import logging

from aiogram import Bot
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.api.deps import get_session_without_commit, get_bot
from app.api.docs.Consts.default_telegram_errors import TELEGRAM_API_ERROR_RESPONSES
from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_human_status import HttpHumanStatusCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.response import ResponseEnvelope, MetaBlockExample
from app.api.docs.common_responses import common_responses
from app.api.schemas.response import (ResponseModelSuccessExample, ErrorResponseBlockExample,
                                      ResponseConfig)
from app.api.utils.db_api_error_handler import db_api_error_handler
from app.api.utils.telegram_handler import telegram_api_error_handler
from app.main_dao.models import TgUser

logger = logging.getLogger(__name__)
router = APIRouter()


class PingResponseData(BaseModel):
    pong: bool = Field(...,
                       description="Флаг, подтверждающий доступность сервиса")
    database_user_count: int = Field(...,
                                     description="Общее количество пользователей в таблице телеграмм-пользователей")
    bot_first_name: str = Field(...,
                                description="Название Telegram-бота.")

    @staticmethod
    def example() -> dict:
        return PingResponseData(pong=True, database_user_count=12345, bot_first_name="Мой Telegram Bot").model_dump()


PING_RESPONSES_DOCS = ResponseConfig(
    success={
        HttpStatusCode.OK: ResponseModelSuccessExample(
            meta=MetaBlockExample(
                status=HttpHumanStatusCode.SUCCESS,
                http_status=HttpStatusCode.OK,
                code=AppResponseCode.SYS_200,
                message="API функционирует корректно. Подключение к базе данных успешно. Телеграмм бот доступен."
            ),
            data=PingResponseData.example(),
            description="Сервис доступен, способен выполнять SQL-запросы к БД, подключение к Telegram Bot установлено"
        )
    },
    error=ErrorResponseBlockExample(
        errors=TELEGRAM_API_ERROR_RESPONSES
    )
)

PING_ENDPOINT_DESCRIPTION = ("Эндпоинт предназначен для проверки доступности и базовой работоспособности API-сервиса. "
                             "Возвращает флаг доступности, количество пользователей в базе данных и название Telegram Bot. "
                             "Может использоваться как healthcheck для мониторинга.")


@router.post("/ping",
             response_model=ResponseEnvelope,
             responses=common_responses(path_suffix="/ping", api_version="v1", response_config=PING_RESPONSES_DOCS),
             summary="Проверка доступности API",
             description=PING_ENDPOINT_DESCRIPTION,
             operation_id="pingSystemHealthCheck",
             response_model_exclude_none=False)
async def ping(request: Request,
               session: AsyncSession = Depends(get_session_without_commit)) -> JSONResponse:
    user_count = 0
    async with db_api_error_handler() as db_ctx:
        result = await session.execute(select(func.count()).select_from(TgUser))
        user_count = result.scalar_one()

    if db_ctx.result:
        return JSONResponse(
            status_code=db_ctx.result["http_status"],
            content=ResponseEnvelope.error(request=request,
                                           message=db_ctx.result["message"],
                                           http_status=db_ctx.result["http_status"],
                                           code=f"DB_{db_ctx.result["http_status"]}"
                                           ).model_dump())

    async with telegram_api_error_handler() as tg_ctx:
        bot: Bot = get_bot()
        bot_me = await bot.get_me()

    if tg_ctx.result:
        return JSONResponse(status_code=tg_ctx.result["http_status"],
                            content=ResponseEnvelope.error(
                                request=request,
                                message=tg_ctx.result["message"],
                                http_status=tg_ctx.result["http_status"],
                                code=f"DB_{tg_ctx.result["http_status"]}"
                            ).model_dump())

    return_data = PingResponseData(pong=True, database_user_count=user_count, bot_first_name=bot_me.first_name)

    return JSONResponse(status_code=HttpStatusCode.OK,
                        content=ResponseEnvelope.success(
                            request=request,
                            data=return_data.model_dump(),
                            code=f"DB_{HttpStatusCode.OK}",
                            message="API функционирует корректно. Подключение к базе данных успешно. Телеграмм бот доступен."
                        ).model_dump())
