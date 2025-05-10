from typing import Dict, Optional
from datetime import datetime

from app.api.docs.errors_const import default_error_descriptions, default_error_messages
from app.api.schemas.response import ResponseEnvelope
from app.config.settings import settings
from app.api.schemas.response import ResponseModelSuccessExample, ResponseModelErrorExample, ResponseConfig


def common_responses(path_suffix: str = '/endpoint',
                     api_version: str = 'v1',
                     response_config: Optional[ResponseConfig] = None) -> Dict[int, Dict]:

    path = f"/api/{api_version}{path_suffix}"
    timestamp = datetime.now(settings.DEFAULT_TZ).isoformat()

    # 400, 401, 403, 404, 405, 408, 409, 410, 411, 412, 413, 414, 415, 422, 426, 429, 500, 501, 502, 503, 504, 505
    allowed_code_errors: tuple[int] = (500,)   # Коды ошибок для каждого метода по умолчанию

    responses: Dict[int, Dict] = {}

    custom_errors: Dict[int, ResponseModelErrorExample] = {}
    if response_config and response_config.error:
        custom_errors = response_config.error.errors

    error_codes = set(custom_errors.keys()) | set(allowed_code_errors)

    for http_status in sorted(error_codes):
        default_description = default_error_descriptions.get(http_status, f"HTTP статус-код: {http_status}")
        default_message = default_error_messages.get(http_status, f"ОHTTP статус-код: {http_status}")

        error_obj = custom_errors.get(
            http_status,
            ResponseModelErrorExample(
                message=default_message,
                description=default_description
            )
        )

        responses[http_status] = {
            "model": ResponseEnvelope,
            "description": error_obj.description,
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "http_status": http_status,
                        "message": error_obj.message,
                        "data": None,
                        "timestamp": timestamp,
                        "path": path
                    }
                }
            }
        }

    success: Dict[int, ResponseModelSuccessExample] = {}
    if response_config:
        success = response_config.success

    for http_status, cfg in success.items():
        responses[http_status] = {
            "model": ResponseEnvelope,
            "description": cfg.description,
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "http_status": http_status,
                        "message": cfg.message,
                        "data": cfg.data,
                        "timestamp": timestamp,
                        "path": path
                    }
                }
            }
        }
    return responses