from app.api.docs.Enums.http_status import HttpStatusCode

SUCCESS_MESSAGES = {
    HttpStatusCode.OK: "Запрос выполнен успешно.",
    HttpStatusCode.CREATED: "Ресурс успешно создан.",
    HttpStatusCode.NO_CONTENT: "Запрос завершён. Ответ без тела.",
}

SUCCESS_DESCRIPTIONS = {
    HttpStatusCode.OK: "Успешный ответ с полезной нагрузкой.",
    HttpStatusCode.CREATED: "Ресурс был создан и возвращён.",
    HttpStatusCode.NO_CONTENT: "Операция завершена. Тело ответа отсутствует.",
}