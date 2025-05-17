from app.dto.models.User._UserBase import _UserBase


class SUserCreate(_UserBase):
    """
    Pydantic-схема добавления нового Telegram-пользователя.

    Attributes:
        telegram_id: Телеграмм-айди пользователя
        first_name: Имя пользователя в Telegram
        last_name: Фамилия пользователя в Telegram
        username: Ссылка на пользователя в Telegram
        is_premium: Есть ли у пользователя премиум-подписка в Telegram
    """
    telegram_id: int
