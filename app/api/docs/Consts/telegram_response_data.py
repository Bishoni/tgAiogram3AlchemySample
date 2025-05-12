from app.api.docs.Enums.http_status import HttpStatusCode

default_start = "Telegram Bot API"

TELEGRAM_API_ERROR_MESSAGES = {
    HttpStatusCode.BAD_REQUEST: f"[{default_start}] Неверный запрос к Telegram API.",
    HttpStatusCode.UNAUTHORIZED: f"[{default_start}] Недействительный токен Telegram Bot.",
    HttpStatusCode.FORBIDDEN: f"[{default_start}] Telegram Bot заблокирован или удалён из чата.",
    HttpStatusCode.NOT_FOUND: f"[{default_start}] Пользователь или чат Telegram не найден. Вероятно, пользователь не инициализировал диалог с ботом.",
    HttpStatusCode.CONFLICT: f"[{default_start}] Конфликт состояний Telegram API.",
    HttpStatusCode.PAYLOAD_TOO_LARGE: f"[{default_start}] Размер вложения превышает допустимый лимит Telegram API.",
    HttpStatusCode.UNPROCESSABLE_ENTITY: f"[{default_start}] Ошибка валидации запроса к Telegram.",
    HttpStatusCode.TOO_MANY_REQUESTS: f"[{default_start}] Превышен лимит запросов к Telegram API.",
    HttpStatusCode.INTERNAL_SERVER_ERROR: f"[{default_start}] Неизвестная ошибка Telegram API.",
    HttpStatusCode.BAD_GATEWAY: f"[{default_start}] Плохой шлюз – ошибка на стороне Telegram.",
    HttpStatusCode.SERVICE_UNAVAILABLE: f"[{default_start}] Telegram API временно недоступен.",
    HttpStatusCode.GATEWAY_TIMEOUT: f"[{default_start}] Истекло время ожидания Telegram API.",
}

TELEGRAM_API_ERROR_DESCRIPTIONS = {
    HttpStatusCode.BAD_REQUEST: f"[`{default_start}`] `400 Bad Request` – **Переданный запрос некорректен по структуре.** <br><br>"
        "Проверьте параметры, типы данных и соответствие документации Telegram.",

    HttpStatusCode.UNAUTHORIZED: f"[{default_start}] Недействительный токен Telegram Bot.",

    HttpStatusCode.FORBIDDEN: f"[`{default_start}`] `403 Forbidden` – **Бот лишён доступа к чату или пользователю.** <br><br>"
        "Наиболее вероятно – пользователь удалил чат или заблокировал бота.",

    HttpStatusCode.NOT_FOUND: f"[`{default_start}`] `404 Not Found` – **Указанный `user_id` или `chat_id` не существует или неактивен.** <br><br>"
        "Проверьте, начал ли пользователь диалог с ботом и актуален ли идентификатор.",

    HttpStatusCode.CONFLICT: f"[`{default_start}`] `409 Conflict` – **Произошёл конфликт с текущим состоянием ресурса.** <br><br>"
        "Возможны параллельные запросы, гонка данных или нарушение согласованности.",

    HttpStatusCode.PAYLOAD_TOO_LARGE: f"[{default_start}] Размер вложения превышает допустимый лимит Telegram API.",

    HttpStatusCode.UNPROCESSABLE_ENTITY: f"[`{default_start}`] `422 Unprocessable Entity` – **Некорректные значения одного или нескольких параметров.** <br><br>"
        "Проверьте типы, ограничения и соответствие требованиям Telegram API.",

    HttpStatusCode.TOO_MANY_REQUESTS: f"[`{default_start}`] `429 Too Many Requests` – **Превышена частота запросов к Telegram API.**",

    HttpStatusCode.INTERNAL_SERVER_ERROR: "`500 Internal Server Error` – **Непредвиденное исключение в логике приложения.** <br><br>"
        "Ошибка может быть вызвана необработанным состоянием, некорректной логикой, зависимостями или внешними сбоями. "
        "Проверьте трассировку в логах (`traceback`) для диагностики. "
        "Если ошибка воспроизводится стабильно — требуется корректировка кода или инфраструктуры.",

    HttpStatusCode.BAD_GATEWAY: f"[`{default_start}`] `502 Bad Gateway` – **Telegram вернул некорректный ответ.** <br><br>"
        "Возможны проблемы с сервером Telegram или сетевыми шлюзами.",

    HttpStatusCode.SERVICE_UNAVAILABLE: f"[`{default_start}`] `503 Service Unavailable` – **Telegram API перегружен или проходит техническое обслуживание.** <br><br>"
        "Повторите попытку позже.",

    HttpStatusCode.GATEWAY_TIMEOUT: f"[`{default_start}`] `504 Gateway Timeout` – **Telegram API не ответил в пределах допустимого времени ожидания.** <br><br>"
        "Проверьте сетевое соединение или повторите запрос позже.",
}

TELEGRAM_API_SUCCESS_MESSAGES = {
    HttpStatusCode.OK: f"[{default_start}] Успешно. Запрос обработан.",
    HttpStatusCode.CREATED: f"[{default_start}] Объект успешно создан.",
    HttpStatusCode.NO_CONTENT: f"[{default_start}] Успешно. Ответ без тела."
}

TELEGRAM_API_SUCCESS_DESCRIPTIONS = {
    HttpStatusCode.OK: f"[`{default_start}`] `200 OK` – Запрос выполнен успешно. Возвращены данные.",
    HttpStatusCode.CREATED: f"[`{default_start}`] `201 Created` – Новый объект создан в Telegram.",
    HttpStatusCode.NO_CONTENT: f"[`{default_start}`] `204 No Content` – Запрос завершён, но тело ответа отсутствует."
}