from app.dto.Models.Admin._AdminBase import _AdminBase


class SAdmin(_AdminBase):
    """
    Основная Pydantic-схема данных администратора.

    Attributes:
        telegram_id: Телеграмм-айди пользователя
        permission_level: Уровень разрешений администратора
        is_active: Активна ли админка в данный момент
        created_at: Дата регистрации пользователя
        updated_at: Дата последней актуализации информации о пользователе
    """
    telegram_id: int
