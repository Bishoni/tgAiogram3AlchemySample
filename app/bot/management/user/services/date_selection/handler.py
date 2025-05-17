from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.management.user.services.date_selection.main import handle_callback_element_edit_date, \
    handle_callback_element_date_day, handle_callback_element_date_prev, handle_callback_element_date_next, \
    handle_callback_element_date_cancel, handle_callback_element_date_confirm, handle_callback_calendar

router = Router(name='user_date_selection')



#region Изменение даты

@router.callback_query(F.data == "calendar")
async def callback_calendar(callback: CallbackQuery, state: FSMContext):
    """Изменение даты элемента"""
    await handle_callback_calendar(callback, state)


@router.callback_query(F.data.startswith("element_edit_date_"))
async def callback_element_edit_date(callback: CallbackQuery, state: FSMContext):
    """Изменение даты элемента"""
    await handle_callback_element_edit_date(callback, state)


@router.callback_query(F.data.startswith("element_date_day_"))
async def callback_element_date_day(callback: CallbackQuery, state: FSMContext):
    """Выбор даты из календаря"""
    await handle_callback_element_date_day(callback, state)


@router.callback_query(F.data.startswith("element_date_prev_"))
async def callback_element_date_prev(callback: CallbackQuery, state: FSMContext):
    """Предыдущий месяц"""
    await handle_callback_element_date_prev(callback, state)


@router.callback_query(F.data.startswith("element_date_next_"))
async def callback_element_date_next(callback: CallbackQuery, state: FSMContext):
    """Следующий месяц"""
    await handle_callback_element_date_next(callback, state)


@router.callback_query(F.data.startswith("element_date_cancel"))
async def callback_element_date_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена выбора даты"""
    await handle_callback_element_date_cancel(callback, state)


@router.callback_query(F.data.startswith("element_date_confirm"))
async def callback_element_date_confirm(callback: CallbackQuery, state: FSMContext):
    """Подтверждение выбора даты"""
    await handle_callback_element_date_confirm(callback, state)
#endregion

def register_handlers(parent_router: Router):
    parent_router.include_router(router)
