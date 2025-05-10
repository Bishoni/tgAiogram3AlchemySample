from app.api.schemas.response import ResponseModelErrorExample

default_start = "Telegram Bot API"
TELEGRAM_API_ERROR_MESSAGES = {
    400: f"[{default_start}] Неверный запрос к Telegram API.",
    401: f"[{default_start}] Недействительный токен Telegram Bot.",
    403: f"[{default_start}] Telegram Bot заблокирован или удалён из чата.",
    404: f"[{default_start}] Пользователь или чат Telegram не найден. Вероятно, пользователь не инициализировал диалог с ботом.",
    409: f"[{default_start}] Конфликт состояний Telegram API.",
    413: f"[{default_start}] Размер вложения превышает допустимый лимит Telegram API.",
    422: f"[{default_start}] Ошибка валидации запроса к Telegram.",
    429: f"[{default_start}] Превышен лимит запросов к Telegram API.",
    500: f"[{default_start}] Неизвестная ошибка Telegram API.",
    502: f"[{default_start}] Плохой шлюз – ошибка на стороне Telegram.",
    503: f"[{default_start}] Telegram API временно недоступен.",
    504: f"[{default_start}] Истекло время ожидания Telegram API.",
}

TELEGRAM_API_ERROR_RESPONSES = {
    400: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[400],
        description=(
            f"[`{default_start}`] `400 Bad Request` – Переданный запрос некорректен по структуре. "
            "Проверьте параметры, типы данных и соответствие документации Telegram."
        )
    ),
    403: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[403],
        description=(
            f"[`{default_start}`] `403 Forbidden` – Бот лишён доступа к чату или пользователю. "
            "Наиболее вероятно – пользователь удалил чат или заблокировал бота."
        )
    ),
    404: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[404],
        description=(
            f"[`{default_start}`] `404 Not Found` – Указанный `user_id` или `chat_id` не существует или неактивен. "
            "Проверьте, начал ли пользователь диалог с ботом и актуален ли идентификатор."
        )
    ),
    409: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[409],
        description=(
            f"[`{default_start}`] `409 Conflict` – Произошёл конфликт с текущим состоянием ресурса. "
            "Возможны параллельные запросы, гонка данных или нарушение согласованности."
        )
    ),
    422: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[422],
        description=(
            f"[`{default_start}`] `422 Unprocessable Entity` – Некорректные значения одного или нескольких параметров. "
            "Проверьте типы, ограничения и соответствие требованиям Telegram API."
        )
    ),
    429: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[429],
        description=(
            f"[`{default_start}`] `429 Too Many Requests` – Превышена частота запросов к Telegram API. "
            "Следует реализовать ограничение (`rate limit`) и повторить попытку позже."
        )
    ),
    500: ResponseModelErrorExample(
        message="Внутренняя ошибка сервера.",
        description=(
            "`500 Internal Server Error` – Непредвиденное исключение в логике приложения. "
            "Ошибка может быть вызвана необработанным состоянием, некорректной логикой, зависимостями или внешними сбоями. "
            "Проверьте трассировку в логах (`traceback`) для диагностики. "
            "Если ошибка воспроизводится стабильно — требуется корректировка кода или инфраструктуры."
        )
    ),
    502: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[502],
        description=(
            f"[`{default_start}`] `502 Bad Gateway` – Telegram вернул некорректный ответ. "
            "Возможны проблемы с сервером Telegram или сетевыми шлюзами (например, прокси)."
        )
    ),
    503: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[503],
        description=(
            f"[`{default_start}`] `503 Service Unavailable` – Telegram API перегружен или проходит техническое обслуживание. "
            "Повторите попытку позже."
        )
    ),
    504: ResponseModelErrorExample(
        message=TELEGRAM_API_ERROR_MESSAGES[504],
        description=(
            f"[`{default_start}`] `504 Gateway Timeout` – Telegram API не ответил в пределах допустимого времени ожидания. "
            "Проверьте сетевое соединение или повторите запрос позже."
        )
    ),
}