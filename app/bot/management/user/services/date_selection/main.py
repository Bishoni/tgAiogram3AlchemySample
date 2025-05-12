from datetime import date, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import logging

from app.bot.management.shared.keyboards.inline import inline_calendar_keyboard

logger = logging.getLogger(__name__)


async def handle_calendar_command(message: Message, state: FSMContext):
    """
    Обработка команды /calendar. Показывает инлайн-календарь.
    """
    today = date.today()

    await message.answer(
        text="📅 Выберите дату:",
        reply_markup=inline_calendar_keyboard(
            year=today.year,
            month=today.month,
            selected_date=None,
            callback_prefix="calendar_"
        )
    )


async def handle_calendar_day_selected(callback: CallbackQuery, state: FSMContext):
    _, _, y, m, d = callback.data.split("_")
    selected = date(int(y), int(m), int(d))
    await state.update_data(selected_date=selected.isoformat())

    await callback.message.edit_reply_markup(
        reply_markup=inline_calendar_keyboard(
            year=selected.year,
            month=selected.month,
            selected_date=selected,
            callback_prefix="calendar_"
        )
    )
    await callback.answer()


async def handle_calendar_prev(callback: CallbackQuery, state: FSMContext):
    _, _, y, m = callback.data.split("_")
    current = date(int(y), int(m), 1)
    prev_month = (current.replace(day=1) - timedelta(days=1)).replace(day=1)

    data = await state.get_data()
    selected = date.fromisoformat(data["selected_date"]) if "selected_date" in data else None

    await callback.message.edit_reply_markup(
        reply_markup=inline_calendar_keyboard(
            year=prev_month.year,
            month=prev_month.month,
            selected_date=selected,
            callback_prefix="calendar_"
        )
    )
    await callback.answer()


async def handle_calendar_next(callback: CallbackQuery, state: FSMContext):
    _, _, y, m = callback.data.split("_")
    current = date(int(y), int(m), 1)
    next_month = (current.replace(day=28) + timedelta(days=4)).replace(day=1)

    data = await state.get_data()
    selected = date.fromisoformat(data["selected_date"]) if "selected_date" in data else None

    await callback.message.edit_reply_markup(
        reply_markup=inline_calendar_keyboard(
            year=next_month.year,
            month=next_month.month,
            selected_date=selected,
            callback_prefix="calendar_"
        )
    )
    await callback.answer()


async def handle_calendar_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer("❌ Отменено")


async def handle_calendar_confirm(callback, state):
    data = await state.get_data()
    selected_str = data.get("selected_date")
    if selected_str:
        selected = date.fromisoformat(selected_str)
        await callback.message.edit_text(f"✅ Вы выбрали: {selected.strftime('%d.%m.%Y')}")
    else:
        await callback.answer("Дата не выбрана", show_alert=True)
    await state.clear()