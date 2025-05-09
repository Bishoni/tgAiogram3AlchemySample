from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from app.api.schemas.response import ResponseEnvelope
from app.api.docs.common_responses import common_responses
from app.actions.services.bot_notify_service import notify_user_by_bot, BotNotifyResult

router = APIRouter()


@router.post(
    "/notify",
    response_model=ResponseEnvelope,
    responses=common_responses(
        "/notify",
        {
            "success": {
                200: {
                    "message": "Сообщение успешно отправлено",
                    "description": "Бот отправил сообщение по переданному user_id",
                    "data": {"notified": True, "user_id": 12345, "message": "Сообщение пользователю"}
                }
            },
            "error": {
                "errors": {
                    500: {
                        "message": "Не удалось отправить сообщение пользователю",
                        "description": "Ошибка отправки. Подробнее – в сообщении к ошибке"
                    },
                    422: {
                        "message": "Описание ошибки валидации",
                        "description": "Ошибка валидации"
                    }
                }
            }
        }
    ),
    summary="Уведомить пользователя",
    description="Отправляет сообщение пользователю в Telegram по его user_id.")
async def notify_user(request: Request,
                      user_id: int = Query(..., description="Telegram user_id"),
                      message: str = Query(..., description="Сообщение пользователю",
                                           min_length=1, max_length=4000,
                                           pattern=r"^[А-Яа-яA-Za-z0-9\s\.\,\!\?\-]+$")):
    result: BotNotifyResult = await notify_user_by_bot(user_id=user_id, text=message)
    # todo: кастомые валидации
    if result["ok"]:
        return_data = {"success": True, "user_id": user_id, "message": message}
        envelope = ResponseEnvelope.success(data=return_data, path=str(request.url), message=result["message"])
        return JSONResponse(status_code=200, content=envelope.model_dump())

    envelope = ResponseEnvelope.error(path=str(request.url), message=result["message"], code=500)
    return JSONResponse(status_code=500, content=envelope.model_dump())
