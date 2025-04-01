from datetime import datetime
from pydantic import BaseModel, Field


class _AdminBase(BaseModel):
    """
    Pydantic-схема общих данных администратора.

    Attributes:
        permission_level: Уровень разрешений администратора
        is_active: Активна ли админка в данный момент
        created_at: Дата регистрации пользователя
        updated_at: Дата последней актуализации информации о пользователе
    """
    permission_level: int = Field(default=0)
    is_active: bool | None = Field(default=False)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
