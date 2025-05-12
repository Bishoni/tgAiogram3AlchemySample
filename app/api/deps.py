from typing import Any, AsyncGenerator

from aiogram import Bot

from app.bot.create_bot import bot
from app.main_dao.base import async_session_scope


def get_bot() -> Bot:
    return bot


async def get_session_with_commit() -> AsyncGenerator[Any, Any]:
    async with async_session_scope() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session_without_commit() -> AsyncGenerator[Any, Any]:
    async with async_session_scope() as session:
        yield session
