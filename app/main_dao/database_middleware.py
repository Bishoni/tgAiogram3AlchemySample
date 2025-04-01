from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from app.main_dao.base import async_session_scope


class BaseDatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       event: Message | CallbackQuery, data: Dict[str, Any]) -> Any:

        async with async_session_scope() as session:
            self.set_session(data, session)
            result = await handler(event, data)
            await self.after_handler(session)
            return result

    def set_session(self, data: Dict[str, Any], session) -> None:
        """Метод для установки сессии в словарь данных."""
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    async def after_handler(self, session) -> None:
        """Метод для выполнения действий после вызова хендлера."""
        pass


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        data['session_without_commit'] = session


class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        data['session_with_commit'] = session

    async def after_handler(self, session) -> None:
        await session.commit()
