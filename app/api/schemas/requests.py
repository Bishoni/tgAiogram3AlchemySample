from fastapi import Query


query_telegram_user_id: int = Query(...,
                                    description="Telegram API user ID",
                                    example=123456789)

query_telegram_message: str = Query(...,
                                    description="Сообщение пользователю",
                                    min_length=1,
                                    max_length=4000,
                                    pattern=r"^[А-Яа-яA-Za-z0-9\s.,?-]+$",
                                    example="Пример сообщения")
