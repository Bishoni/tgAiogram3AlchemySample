from enum import Enum

from app.api.docs.Consts.telegram_response_data import TELEGRAM_API_ERROR_MESSAGES


class AppResponseCode(str, Enum):
    # --- Telegram-related Errors ---
    TG_400 = "TG_400"
    TG_401 = "TG_401"
    TG_403 = "TG_403"
    TG_404 = "TG_404"
    TG_405 = "TG_405"
    TG_408 = "TG_408"
    TG_409 = "TG_409"
    TG_410 = "TG_410"
    TG_411 = "TG_411"
    TG_412 = "TG_412"
    TG_413 = "TG_413"
    TG_414 = "TG_414"
    TG_415 = "TG_415"
    TG_422 = "TG_422"
    TG_426 = "TG_426"
    TG_429 = "TG_429"
    TG_500 = "TG_500"
    TG_501 = "TG_501"
    TG_502 = "TG_502"
    TG_503 = "TG_503"
    TG_504 = "TG_504"
    TG_505 = "TG_505"

    # --- DB-related Errors ---
    DB_400 = "DB_400"
    DB_401 = "DB_401"
    DB_403 = "DB_403"
    DB_404 = "DB_404"
    DB_405 = "DB_405"
    DB_408 = "DB_408"
    DB_409 = "DB_409"
    DB_410 = "DB_410"
    DB_411 = "DB_411"
    DB_412 = "DB_412"
    DB_413 = "DB_413"
    DB_414 = "DB_414"
    DB_415 = "DB_415"
    DB_422 = "DB_422"
    DB_426 = "DB_426"
    DB_429 = "DB_429"
    DB_500 = "DB_500"
    DB_501 = "DB_501"
    DB_502 = "DB_502"
    DB_503 = "DB_503"
    DB_504 = "DB_504"
    DB_505 = "DB_505"

    # --- System-level Errors ---
    SYS_400 = "SYS_400"
    SYS_401 = "SYS_401"
    SYS_403 = "SYS_403"
    SYS_404 = "SYS_404"
    SYS_405 = "SYS_405"
    SYS_408 = "SYS_408"
    SYS_409 = "SYS_409"
    SYS_410 = "SYS_410"
    SYS_411 = "SYS_411"
    SYS_412 = "SYS_412"
    SYS_413 = "SYS_413"
    SYS_414 = "SYS_414"
    SYS_415 = "SYS_415"
    SYS_422 = "SYS_422"
    SYS_426 = "SYS_426"
    SYS_429 = "SYS_429"
    SYS_500 = "SYS_500"
    SYS_501 = "SYS_501"
    SYS_502 = "SYS_502"
    SYS_503 = "SYS_503"
    SYS_504 = "SYS_504"
    SYS_505 = "SYS_505"

    SYS_000 = "SYS_000"

    # --- Success Codes ---
    OK_200 = "OK_200"
    OK_201 = "OK_201"
    OK_204 = "OK_204"

    TG_200 = "TG_200"
    TG_201 = "TG_201"
    TG_204 = "TG_204"

    SYS_200 = "SYS_200"
    DB_200 = "DB_200"
    DB_201 = "DB_201"
    DB_204 = "DB_204"


    # --- Generics ---
    GENERIC_RESPONSE = "RESPONSE_DEFAULT"
    GENERIC_SUCCESS = "SUCCESS_DEFAULT"
    GENERIC_ERROR = "ERROR_DEFAULT"

    # --- Specials ---
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CRITICAL_ERROR = "CRITICAL_ERROR"
    BASIC_HTTP_ERROR = "BASIC_HTTP_ERROR"

    def message(self) -> str:
        return ERROR_CODE_MESSAGE.get(self.value, "Неизвестный локальный код ошибки/успеха.")


ERROR_CODE_MESSAGE = {
    AppResponseCode.TG_400.value: TELEGRAM_API_ERROR_MESSAGES[400],
    AppResponseCode.TG_403.value: TELEGRAM_API_ERROR_MESSAGES[403],
    AppResponseCode.TG_404.value: TELEGRAM_API_ERROR_MESSAGES[404],
    AppResponseCode.TG_409.value: TELEGRAM_API_ERROR_MESSAGES[409],
    AppResponseCode.TG_422.value: TELEGRAM_API_ERROR_MESSAGES[422],
    AppResponseCode.TG_429.value: TELEGRAM_API_ERROR_MESSAGES[429],
    AppResponseCode.TG_502.value: TELEGRAM_API_ERROR_MESSAGES[502],
    AppResponseCode.TG_503.value: TELEGRAM_API_ERROR_MESSAGES[503],
    AppResponseCode.TG_504.value: TELEGRAM_API_ERROR_MESSAGES[504],

    AppResponseCode.SYS_500.value: "Внутренняя ошибка сервера.",
    AppResponseCode.SYS_000.value: "Непредвиденная системная ошибка.",

    AppResponseCode.OK_200.value: "Операция успешно завершена.",
    AppResponseCode.OK_201.value: "Ресурс создан.",
    AppResponseCode.OK_204.value: "Успешно, но тело ответа отсутствует.",
}
