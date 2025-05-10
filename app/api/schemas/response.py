from pydantic import BaseModel, Field
from fastapi import Request
from typing import Literal, Dict, Any, Optional, TypedDict
from datetime import datetime

from app.config.settings import settings

# todo: добавить локальные возвраты "code"
# todo: сделать отображение data: null в json
class ResponseEnvelope(BaseModel):
    status: Literal["success", "error"] = Field(...,
                                                description="Статус результата запроса: 'success' — если успешно, 'error' — если произошла ошибка.")

    http_status: int = Field(...,
                      description="HTTP статус-код, соответствующий результату запроса (например, 200, 400, 404, 500).")

    message: str = Field(...,
                         description="Краткое человеко-читаемое сообщение о результате запроса или описании ошибки.")

    data: Optional[Dict[str, Any]] = Field(None,
        description="Полезная нагрузка ответа.")

    timestamp: str = Field(...,
                           description="Дата и время формирования ответа на сервере, в ISO формате.")

    path: str = Field(...,
                      description="Относительный путь запроса, приведший к данному ответу.")

    @classmethod
    def success(cls,
                request: Request,
                data: Dict[str, Any],
                message: str = "Success",
                http_status: int = 200) -> "ResponseEnvelope":
        now = datetime.now(settings.DEFAULT_TZ).isoformat()
        return cls(status="success",
                   http_status=http_status,
                   message=message,
                   data=data,
                   timestamp=now,
                   path=request.url.path)

    @classmethod
    def error(cls,
              request: Request,
              message: str = "Error",
              http_status: int = 400) -> "ResponseEnvelope":
        now = datetime.now(settings.DEFAULT_TZ).isoformat()
        return cls(status="error",
                   http_status=http_status,
                   message=message,
                   data=None,
                   timestamp=now,
                   path=request.url.path)


class ResponseModelSuccessExample(BaseModel):
    message: str
    description: str
    data: dict


class ResponseModelErrorExample(BaseModel):
    message: str
    description: str


class ErrorResponseBlockExample(BaseModel):
    errors: Dict[int, ResponseModelErrorExample]


class ResponseConfig(BaseModel):
    success: Dict[int, ResponseModelSuccessExample]
    error: ErrorResponseBlockExample


class ResponseFromTelegramLogic(TypedDict):
    message: str
    http_status: int
