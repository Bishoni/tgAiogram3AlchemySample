from app.dto.models.User._UserBase import _UserBase


class SUser(_UserBase):
    """
    Основная Pydantic-схема данных Telegram-пользователя.

    Attributes:
        telegram_id: Телеграмм-айди пользователя
        first_name: Имя пользователя в Telegram
        last_name: Фамилия пользователя в Telegram
        username: Ссылка на пользователя в Telegram
        is_premium: Есть ли у пользователя премиум-подписка в Telegram
        created_at: Дата регистрации пользователя
        updated_at: Дата последней актуализации информации о пользователе
    """
    telegram_id: int
