import logging
import traceback

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field

from app.api.docs.Consts.default_telegram_errors import TELEGRAM_API_ERROR_RESPONSES
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.requests import query_telegram_user_id, query_telegram_message
from app.api.schemas.response import ResponseEnvelope, ResponseFromAnotherLogic, MetaBlockExample
from app.api.docs.common_responses import common_responses
from app.actions.services.bot_notify_service import notify_user_by_bot
from app.api.schemas.response import ResponseModelSuccessExample, ErrorResponseBlockExample, ResponseConfig

logger = logging.getLogger(__name__)
router = APIRouter()


class NotifyResponseData(BaseModel):
    notified: bool = Field(..., description="Флаг, подтверждающий, было ли сообщение отправлено")
    user_id: int = Field(..., description="Идентификатор пользователя Telegram")
    message: str = Field(..., description="Текст отправленного сообщения")

    @staticmethod
    def example() -> dict:
        return NotifyResponseData(
            notified=True,
            user_id=12345,
            message="Сообщение пользователю"
        ).model_dump()


NOTIFY_RESPONSES_DOCS = ResponseConfig(
    success={
        HttpStatusCode.OK: ResponseModelSuccessExample(
            meta=MetaBlockExample(
                status="success",
                http_status=HttpStatusCode.OK,
                message="Сообщение успешно отправлено"
            ),
            data=NotifyResponseData.example(),
            description="Бот отправил сообщение в Telegram по указанному user_id.",
        )
    },
    error=ErrorResponseBlockExample(
        errors=TELEGRAM_API_ERROR_RESPONSES
    )
)


@router.get("/notify",
             response_model=ResponseEnvelope,
             responses=common_responses(path_suffix="/notify", api_version="v1", response_config=NOTIFY_RESPONSES_DOCS),
             summary="Отправить сообщение пользователю",
             description=(
                     "Отправляет указанное текстовое сообщение пользователю Telegram по его user_id. "
                     "Используется встроенный Telegram-бот, идентификатор и токен которого настроены в конфигурации."
             ),
             operation_id="notifyTelegramUser",
             tags=["bot"])
async def notify_user(request: Request,
                      user_id: int = query_telegram_user_id,
                      message: str = query_telegram_message) -> JSONResponse:
    result: ResponseFromAnotherLogic = await notify_user_by_bot(user_id=user_id, text=message)

    if result["http_status"] == HttpStatusCode.OK:
        return_data = NotifyResponseData(
            notified=True,
            user_id=user_id,
            message=message
        )
        return_content = ResponseEnvelope.success(
            request=request,
            data=return_data.model_dump(),
            message=result["message"],
            code=result["code"]
        )
        return JSONResponse(status_code=result["http_status"], content=return_content.model_dump())

    return_content = ResponseEnvelope.error(
        request=request,
        message=result["message"],
        http_status=result["http_status"],
        code=result["code"]
    )
    return JSONResponse(status_code=result["http_status"], content=return_content.model_dump())
