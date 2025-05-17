from app.api.docs.consts.telegram_response_data import TELEGRAM_API_SUCCESS_MESSAGES, TELEGRAM_API_SUCCESS_DESCRIPTIONS
from app.api.docs.enums.app_response_codes import AppResponseCode
from app.api.docs.enums.http_status import HttpStatusCode
from app.api.docs.enums.http_human_status import HttpHumanStatusCode
from app.api.schemas.response import ResponseModelSuccessExample, MetaBlockExample

TELEGRAM_API_SUCCESS_RESPONSES = {
    HttpStatusCode.OK: ResponseModelSuccessExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.SUCCESS,
            http_status=HttpStatusCode.OK,
            code=AppResponseCode.TG_200,
            message=TELEGRAM_API_SUCCESS_MESSAGES[HttpStatusCode.OK]
        ),
        data={},
        description=TELEGRAM_API_SUCCESS_DESCRIPTIONS[HttpStatusCode.OK]
    ),
    HttpStatusCode.CREATED: ResponseModelSuccessExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.SUCCESS,
            http_status=HttpStatusCode.CREATED,
            code=AppResponseCode.TG_201,
            message=TELEGRAM_API_SUCCESS_MESSAGES[HttpStatusCode.CREATED]
        ),
        data={},
        description=TELEGRAM_API_SUCCESS_DESCRIPTIONS[HttpStatusCode.CREATED]
    ),
    HttpStatusCode.NO_CONTENT: ResponseModelSuccessExample(
        meta=MetaBlockExample(
            status=HttpHumanStatusCode.SUCCESS,
            http_status=HttpStatusCode.NO_CONTENT,
            code=AppResponseCode.TG_204,
            message=TELEGRAM_API_SUCCESS_MESSAGES[HttpStatusCode.NO_CONTENT]
        ),
        data={},
        description=TELEGRAM_API_SUCCESS_DESCRIPTIONS[HttpStatusCode.NO_CONTENT]
    )
}
