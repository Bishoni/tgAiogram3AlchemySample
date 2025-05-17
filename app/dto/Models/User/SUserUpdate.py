from app.dto.models.User._UserBase import _UserBase


class SUserUpdate(_UserBase):
    """
    Pydantic-схема обновления данных Telegram-пользователя.

    Attributes:
        first_name: Имя пользователя в Telegram
        last_name: Фамилия пользователя в Telegram
        username: Ссылка на пользователя в Telegram
        is_premium: Есть ли у пользователя премиум-подписка в Telegram
    """
    pass
