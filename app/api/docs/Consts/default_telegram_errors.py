from app.api.docs.Consts.telegram_response_data import TELEGRAM_API_ERROR_MESSAGES, TELEGRAM_API_ERROR_DESCRIPTIONS
from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_human_status import HttpHumanStatusCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.response import ResponseModelErrorExample, MetaBlockExample


TELEGRAM_API_ERROR_RESPONSES = {
    HttpStatusCode.BAD_REQUEST: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.BAD_REQUEST,
            code=AppResponseCode.TG_400,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.BAD_REQUEST]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.BAD_REQUEST]
    ),
    HttpStatusCode.FORBIDDEN: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.FORBIDDEN,
            code=AppResponseCode.TG_403,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.FORBIDDEN]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.FORBIDDEN]
    ),
    HttpStatusCode.NOT_FOUND: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.NOT_FOUND,
            code=AppResponseCode.TG_404,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.NOT_FOUND]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.NOT_FOUND]
    ),
    HttpStatusCode.CONFLICT: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.CONFLICT,
            code=AppResponseCode.TG_409,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.CONFLICT]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.CONFLICT]
    ),
    HttpStatusCode.UNPROCESSABLE_ENTITY: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.UNPROCESSABLE_ENTITY,
            code=AppResponseCode.TG_422,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.UNPROCESSABLE_ENTITY]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.UNPROCESSABLE_ENTITY]
    ),
    HttpStatusCode.TOO_MANY_REQUESTS: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.TOO_MANY_REQUESTS,
            code=AppResponseCode.TG_429,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.TOO_MANY_REQUESTS]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.TOO_MANY_REQUESTS]
    ),
    HttpStatusCode.INTERNAL_SERVER_ERROR: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.INTERNAL_SERVER_ERROR,
            code=AppResponseCode.SYS_500,
            message="Внутренняя ошибка сервера."
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.INTERNAL_SERVER_ERROR]
    ),
    HttpStatusCode.BAD_GATEWAY: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.BAD_GATEWAY,
            code=AppResponseCode.TG_502,
            message=TELEGRAM_API_ERROR_MESSAGES[502]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[502]
    ),
    HttpStatusCode.SERVICE_UNAVAILABLE: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.SERVICE_UNAVAILABLE,
            code=AppResponseCode.TG_503,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.SERVICE_UNAVAILABLE]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.SERVICE_UNAVAILABLE]
    ),
    HttpStatusCode.GATEWAY_TIMEOUT: ResponseModelErrorExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.ERROR,
            http_status=HttpStatusCode.GATEWAY_TIMEOUT,
            code=AppResponseCode.TG_504,
            message=TELEGRAM_API_ERROR_MESSAGES[HttpStatusCode.GATEWAY_TIMEOUT]
        ),
        data=None,
        description=TELEGRAM_API_ERROR_DESCRIPTIONS[HttpStatusCode.GATEWAY_TIMEOUT]
    ),
}
