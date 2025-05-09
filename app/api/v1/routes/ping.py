from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.schemas.response import ResponseEnvelope
from app.api.docs.common_responses import common_responses

router = APIRouter()


@router.get(
    "/ping",
    response_model=ResponseEnvelope,
    responses=common_responses(
        "/ping",
        {
            "success": {
                200: {
                    "message": "Пинг успешен",
                    "description": "Возвращает pong = true, если API_V1 доступно",
                    "data": {
                        "pong": True
                    }
                }
            },
            "error": {
                "errors": {
                    4042: {
                        # "description": "Кастомное описание",
                        "message": "Кастомное сообщение"
                    }
                }
            }
        }
    ),
    summary="Ping endpoint",
    description="Проверяет, активен ли API_V1 и отвечает ли он.")
async def ping(request: Request):
    return_data = {"pong": True}
    return_message = "Пинг успешен"

    envelope = ResponseEnvelope.success(data=return_data, path=str(request.url), message=return_message)
    return JSONResponse(status_code=200, content=envelope.model_dump())
