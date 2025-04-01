from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.management.shared.services.main.main import handler_noop, handler_close_message

router = Router(name='shared_main')

@router.callback_query(F.data.startswith('noop'))
async def callback_noop(callback: CallbackQuery, state: FSMContext):
    """Защита от ошибочного нажатия // Вывод текущей страницы пагинации"""
    await handler_noop(callback, state)


@router.callback_query(F.data == "close_message")
async def callback_close_message(callback: CallbackQuery, state: FSMContext):
    """Закрыть текущее сообщение"""
    await handler_close_message(callback, state)


def register_handlers(parent_router: Router):
    parent_router.include_router(router)
