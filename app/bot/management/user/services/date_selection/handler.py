from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot.management.user.services.date_selection.main import handle_calendar_command, handle_calendar_day_selected, \
    handle_calendar_prev, handle_calendar_next, handle_calendar_cancel, handle_calendar_confirm

router = Router(name='user_date_selection')


@router.message(Command('calendar'))
async def cmd_calendar(message: Message, state: FSMContext):
    """Команда /calendar"""
    await handle_calendar_command(message, state)


@router.callback_query(F.data.startswith("calendar_day_"))
async def calendar_day_selected(callback: CallbackQuery, state: FSMContext):
    """Выбор даты из календаря"""
    await handle_calendar_day_selected(callback, state)


@router.callback_query(F.data.startswith("calendar_prev_"))
async def calendar_prev(callback: CallbackQuery, state: FSMContext):
    """Предыдущий месяц"""
    await handle_calendar_prev(callback, state)


@router.callback_query(F.data.startswith("calendar_next_"))
async def calendar_next(callback: CallbackQuery, state: FSMContext):
    """Следующий месяц"""
    await handle_calendar_next(callback, state)


@router.callback_query(F.data == "calendar_cancel")
async def calendar_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена выбора даты"""
    await handle_calendar_cancel(callback, state)


@router.callback_query(F.data == "calendar_confirm")
async def calendar_confirm(callback: CallbackQuery, state: FSMContext):
    """Подтверждение выбора даты"""
    await handle_calendar_confirm(callback, state)


def register_handlers(parent_router: Router):
    parent_router.include_router(router)
