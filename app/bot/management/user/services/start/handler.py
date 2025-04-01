from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.management.user.services.start.main import handle_start_command


router = Router(name='user_start')


@router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession, state: FSMContext):
    """Команда /start"""
    await handle_start_command(message, session_with_commit, state)


def register_handlers(parent_router: Router):
    parent_router.include_router(router)