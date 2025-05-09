from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
from datetime import datetime
from app.config.settings import settings


class ResponseEnvelope(BaseModel):
    status: Literal["success", "error"] = Field(...,
        description="Статус результата запроса: 'success' — если успешно, 'error' — если произошла ошибка.")

    code: int = Field(...,
        description="HTTP статус-код, соответствующий результату запроса (например, 200, 400, 404, 500).")

    message: str = Field(...,
        description="Краткое человеко-читаемое сообщение о результате запроса или описании ошибки.")

    data: Optional[Dict[str, Any]] = Field(None,
        description="Полезная нагрузка ответа. Присутствует только в случае успешного выполнения запроса.")

    timestamp: str = Field(...,
        description="Дата и время формирования ответа на сервере, в формате 'ДД.ММ.ГГГГ ЧЧ:ММ:СС MSK'.")

    path: str = Field(...,
        description="Полный путь запроса, приведший к данному ответу.")

    @classmethod
    def success(cls,
                data: Dict[str, Any],
                path: str,
                message: str = "Success",
                code: int = 200) -> "ResponseEnvelope":
        now = datetime.now(settings.DEFAULT_TZ).strftime("%d.%m.%Y %H:%M:%S MSK")
        return cls(status="success",
                   code=code,
                   message=message,
                   data=data,
                   timestamp=now,
                   path=path)

    @classmethod
    def error(cls,
              path: str,
              message: str = "Error",
              code: int = 400) -> "ResponseEnvelope":
        now = datetime.now(settings.DEFAULT_TZ).strftime("%d.%m.%Y %H:%M:%S MSK")
        return cls(status="error",
                   code=code,
                   message=message,
                   data=None,
                   timestamp=now,
                   path=path)
