from app.dto.models.Admin._AdminBase import _AdminBase


class SAdminCreate(_AdminBase):
    """
    Pydantic-схема добавления нового администратора

    Attributes:
        telegram_id: Телеграмм-айди пользователя
        permission_level: Уровень разрешений администратора
        is_active: Активна ли админка в данный момент
    """
    telegram_id: int
