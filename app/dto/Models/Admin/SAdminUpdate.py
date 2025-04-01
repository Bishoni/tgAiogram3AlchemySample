from app.dto.Models.Admin._AdminBase import _AdminBase


class SAdminUpdate(_AdminBase):
    """
    Pydantic-схема обновления администратора

    Attributes:
        telegram_id: Телеграмм-айди пользователя
        permission_level: Уровень разрешений администратора
        is_active: Активна ли админка в данный момент
    """
    telegram_id: int
    