from pydantic import BaseModel, Field
from fastapi import Request
from typing import Literal, Dict, Any, Optional, Annotated, Iterator, Tuple
from datetime import datetime
from uuid import uuid4

from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_human_status import HttpHumanStatusCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.config.settings import settings


class MetaBlock(BaseModel):
    status: Literal[HttpHumanStatusCode.SUCCESS, HttpHumanStatusCode.ERROR] = Field(...,
                             description="Статус результата запроса: 'success' — если успешно, 'error' — если произошла ошибка.")
    http_status: int = Field(...,
                             description="HTTP статус-код, соответствующий результату запроса (например, 200, 400, 404, 500).")
    code: str = Field(...,
                             description="Локальный код результата, например USR_001, SYS_500 и т.д.")
    message: str = Field(...,
                             description="Краткое человеко-читаемое сообщение о результате запроса или описании ошибки.")
    timestamp: str = Field(...,
                             description="Дата и время формирования ответа на сервере, в ISO формате.")
    path: str = Field(...,
                             description="Относительный путь запроса, приведший к данному ответу.")
    request_id: str = Field(...,
                             description="Уникальный идентификатор запроса, используется для трассировки и логирования. Генерируется на каждый входящий HTTP-запрос.")


class ResponseEnvelope(BaseModel):
    meta: MetaBlock
    data: Annotated[
        Optional[Dict[str, Any]],
          Field(
              default=None,
              description=(
                  "Полезная нагрузка ответа."
                  "**Поле `data` всегда присутствует в ответе API**. Если полезная нагрузка отсутствует, оно принимает значение `null`, даже если это не отражено в примерах."
              ),
              json_schema_extra={"nullable": True}
          )
    ]

    @classmethod
    def success(cls,
                request: Request,
                data: Optional[Dict[str, Any]] = None,
                message: str = "Успешно",
                code: str = AppResponseCode.GENERIC_SUCCESS,
                http_status: int = HttpStatusCode.OK) -> "ResponseEnvelope":

        return cls(
            meta=MetaBlock(
                status=HttpHumanStatusCode.SUCCESS,
                http_status=http_status,
                code=code,
                message=message,
                timestamp=datetime.now(settings.DEFAULT_TZ).isoformat(),
                path=request.url.path,
                request_id=str(uuid4()),
            ),
            data=data or {},
        )

    @classmethod
    def error(cls,
              request: Request,
              message: str = "Ошибка",
              code: str = AppResponseCode.GENERIC_ERROR,
              http_status: int = HttpStatusCode.INTERNAL_SERVER_ERROR) -> "ResponseEnvelope":
        return cls(
            meta=MetaBlock(
                status=HttpHumanStatusCode.ERROR,
                http_status=http_status,
                code=code,
                message=message,
                timestamp=datetime.now(settings.DEFAULT_TZ).isoformat(),
                path=request.url.path,
                request_id=str(uuid4()),
            ),
            data=None,
        )


class MetaBlockExample(BaseModel):
    status: Literal[HttpHumanStatusCode.SUCCESS, HttpHumanStatusCode.ERROR]
    http_status: int
    code: str = AppResponseCode.GENERIC_RESPONSE
    message: str


class ResponseModelSuccessExample(BaseModel):
    meta: MetaBlockExample
    data: dict
    description: str


class ResponseModelErrorExample(BaseModel):
    meta: MetaBlockExample
    data: Optional[None] = None
    description: str


class ErrorResponseBlockExample(BaseModel):
    errors: Dict[int, ResponseModelErrorExample]


class ResponseConfig(BaseModel):
    success: Dict[int, ResponseModelSuccessExample]
    error: ErrorResponseBlockExample


class ResponseFromAnotherLogic(BaseModel):
    message: str
    http_status: int
    code: str
    data: Optional[dict] = None

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def keys(self) -> Iterator[str]:
        return iter(self.model_fields.keys())  # ✅ modern Pydantic v2 style

    def values(self) -> Iterator[Any]:
        return (getattr(self, k) for k in self.model_fields.keys())

    def items(self) -> Iterator[Tuple[str, Any]]:
        return ((k, getattr(self, k)) for k in self.model_fields.keys())

    def to_dict(self) -> dict:
        return self.model_dump()
