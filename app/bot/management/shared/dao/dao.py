from typing import Literal

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.main_dao.base import BaseDAO
from app.main_dao.models import TgUser, AdminAccount
from sqlalchemy.future import select
import logging


logger= logging.getLogger(__name__)


class TelegramIDMixin:
    async def find_by_telegram_id(self, telegram_id: int) -> object | None:
        """
        Ищет запись в базе по telegram_id.

        Параметры:
            telegram_id (int): Telegram ID записи.

        Возвращает:
            Объект модели или None, если запись не найдена.
        """
        try:
            query = select(self.model).filter_by(telegram_id=telegram_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            logger.debug(f"Пользователь с telegram_id={telegram_id} {'найден' if record else 'не найден'}.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске пользователя telegram_id={telegram_id}: {e}")
            raise


class UserDAO(BaseDAO[TgUser], TelegramIDMixin):
    model = TgUser


class AdminDAO(BaseDAO[AdminAccount], TelegramIDMixin):
    model = AdminAccount
