from typing import Dict, Optional
from datetime import datetime
from uuid import uuid4

from app.api.docs.Consts.errors_const import default_error_descriptions, default_error_messages
from app.api.docs.Consts.success_const import SUCCESS_MESSAGES, SUCCESS_DESCRIPTIONS
from app.api.docs.Enums.http_human_status import HttpHumanStatusCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.response import (
    ResponseEnvelope,
    MetaBlockExample,
    ResponseModelSuccessExample,
    ResponseModelErrorExample,
    ResponseConfig
)
from app.config.settings import settings


def common_responses(path_suffix: str = "/endpoint",
                     api_version: str = "v1",
                     response_config: Optional[ResponseConfig] = None) -> Dict[int, Dict]:
    path = f"/api/{api_version}{path_suffix}"
    timestamp = datetime.now(settings.DEFAULT_TZ).isoformat()
    request_id = str(uuid4())

    allowed_code_errors: tuple[int, ...] = (HttpStatusCode.INTERNAL_SERVER_ERROR,)
    allowed_code_success: tuple[int, ...] = (HttpStatusCode.OK,)

    responses: Dict[int, Dict] = {}

    def build_response_block(_http_status: int, meta: MetaBlockExample, data: Optional[dict], description: str) -> Dict:
        return {
            "model": ResponseEnvelope,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "meta": {
                            **meta.model_dump(),
                            "timestamp": timestamp,
                            "path": path,
                            "request_id": request_id
                        },
                        "data": data
                    }
                }
            }
        }

    custom_errors: Dict[int, ResponseModelErrorExample] = {}
    if response_config and response_config.error:
        custom_errors = response_config.error.errors

    error_codes = set(custom_errors.keys()) | set(allowed_code_errors)

    for http_status in sorted(error_codes):
        default_description = default_error_descriptions.get(http_status, f"HTTP {http_status} – ошибка.")
        default_message = default_error_messages.get(http_status, f"Ошибка (HTTP – {http_status})")

        error_obj = custom_errors.get(
            http_status,
            ResponseModelErrorExample(
                meta=MetaBlockExample(
                    status=HttpHumanStatusCode.ERROR,
                    http_status=http_status,
                    code=f"SYS_{http_status}",
                    message=default_message
                ),
                data=None,
                description=default_description
            )
        )

        responses[http_status] = build_response_block(
            _http_status=http_status,
            meta=error_obj.meta,
            data=None,
            description=error_obj.description
        )

    success_items: Dict[int, ResponseModelSuccessExample] = {}
    if response_config and response_config.success:
        success_items = response_config.success

    success_codes = set(success_items.keys()) | set(allowed_code_success)

    for http_status in sorted(success_codes):
        success_obj = success_items.get(http_status)

        if not success_obj:
            success_obj = ResponseModelSuccessExample(
                meta=MetaBlockExample(
                    status=HttpHumanStatusCode.SUCCESS,
                    http_status=http_status,
                    code=f"OK_{http_status}",
                    message=SUCCESS_MESSAGES.get(http_status, f"Успешно ({http_status})")
                ),
                data={},
                description=SUCCESS_DESCRIPTIONS.get(http_status, f"HTTP {http_status} – стандартный успешный ответ.")
            )

        responses[http_status] = build_response_block(
            _http_status=http_status,
            meta=success_obj.meta,
            data=success_obj.data,
            description=success_obj.description
        )

    return responses
