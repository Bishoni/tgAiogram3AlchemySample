from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class _UserBase(BaseModel):
    """
    Pydantic-схема общих данных Telegram-пользователя.

    Attributes:
        first_name: Имя пользователя в Telegram
        last_name: Фамилия пользователя в Telegram
        username: Ссылка на пользователя в Telegram
        is_premium: Есть ли у пользователя премиум-подписка в Telegram
        created_at: Дата регистрации пользователя
        updated_at: Дата последней актуализации информации о пользователе
    """
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    username: str | None = Field(default=None)
    is_premium: bool | None = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
