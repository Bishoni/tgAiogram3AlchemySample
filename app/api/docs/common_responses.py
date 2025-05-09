from typing import Dict
from datetime import datetime
from app.api.schemas.response import ResponseEnvelope
from app.config.settings import settings


def common_responses(path_suffix: str = '/endpoint', response_config: Dict[str, Dict] = None) -> Dict[int, Dict]:
    base_url = "http://ip:port/api/v1"
    path = f"{base_url}{path_suffix}"

    now = datetime.now(settings.DEFAULT_TZ)
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S MSK")

    default_error_descriptions = {
        # 400: "Некорректный запрос – сервер не может обработать запрос",
        # 404: "Не найдено – указанный ресурс не существует",
        # 409: "Конфликт – конфликт данных с текущим состоянием",
        # 422: "Ошибка валидации – переданные данные недопустимы",
        500: "Внутренняя ошибка сервера – непредвиденная ошибка на стороне сервера",
    }

    responses = {}

    errors = (response_config or {}).get("error", {}).get("errors", {})
    all_error_codes = set(default_error_descriptions.keys()) | set(errors.keys())

    for code in sorted(all_error_codes):
        default_description = default_error_descriptions.get(code, f"Ошибка – {code}")
        error = errors.get(code, {})

        message = error.get("message", f"Сообщение к ошибке – {code}")
        description = error.get("description", default_description)

        responses[code] = {
            "model": ResponseEnvelope,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "code": code,
                        "message": message,
                        "data": None,
                        "timestamp": timestamp,
                        "path": path
                    }
                }
            }
        }

    success_config = (response_config or {}).get("success", {})
    for code, cfg in success_config.items():
        message = cfg.get("message", "Успешно")
        description = cfg.get("description", "Успешный ответ")
        data = cfg.get("data", {"ключ": "значение"})

        responses[code] = {
            "model": ResponseEnvelope,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "code": code,
                        "message": message,
                        "data": data,
                        "timestamp": timestamp,
                        "path": path
                    }
                }
            }
        }

    return responses
