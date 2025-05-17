import random
from datetime import date, timedelta, datetime
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging

from app.bot.management.shared.keyboards.inline import inline_calendar_keyboard, inline_one_button
from app.bot.management.user.services.date_selection.state import UserState
from app.bot.management.user.services.date_selection.utils import TXT_ELEMENT_EDIT_DATE, validate_state
from app.config.settings import settings

logger = logging.getLogger(__name__)


async def handle_callback_calendar(callback: CallbackQuery, state: FSMContext) -> None:
    element_id = random.randint(1, 1000)
    msg_txt = f'Промежуточный элемент для редактирования даты: №<code>{element_id}</code>'
    reply_mk = inline_one_button('Перейти к календарю', f'element_edit_date_{element_id}')
    await state.update_data(element_id=str(element_id))
    await state.set_state(UserState.generic)
    await callback.message.edit_text(msg_txt, reply_markup=reply_mk)


async def handle_callback_element_edit_date(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, _, _element_id = callback.data.split('_')
    element_id = _element_id
    if not await validate_state(callback, state, element_id, True):
        return

    # now = datetime.now().astimezone(settings.DEFAULT_TZ)
    now = datetime(2025, 5, 20, 0, 0, tzinfo=settings.DEFAULT_TZ)
    selected_date = now + timedelta(days=random.randint(1, 3))

    await state.update_data(old_datetime=now.isoformat(), selected_date=selected_date.isoformat())

    selected_date_str = selected_date.strftime('%d.%m.%Y')
    now_date_str = now.strftime('%d.%m.%Y')
    reply_mk = inline_calendar_keyboard(
        calendar_year=now.year,
        calendar_month=now.month,
        selected_date=selected_date,
        callback_prefix='element_date_',
        callback_suffix=f'_{element_id}',
        first_date=now)
    msg_txt = TXT_ELEMENT_EDIT_DATE(element_id, now_date_str, selected_date_str)
    await callback.message.edit_text(msg_txt, reply_markup=reply_mk)


async def handle_callback_element_date_day(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, _, y, m, d, _element_id = callback.data.split("_")
    selected = date(int(y), int(m), int(d))
    if not await validate_state(callback, state, _element_id, True):
        return

    await state.update_data(selected_date=selected.isoformat())
    data = await state.get_data()
    old_date = datetime.fromisoformat(data['old_datetime']).astimezone(settings.DEFAULT_TZ)
    element_date_str = old_date.strftime('%d.%m.%Y')
    element_selected_date_str = selected.strftime('%d.%m.%Y')
    msg_txt = TXT_ELEMENT_EDIT_DATE(_element_id, element_date_str, element_selected_date_str)

    await callback.message.edit_text(
        text=msg_txt,
        reply_markup=inline_calendar_keyboard(
            calendar_year=selected.year,
            calendar_month=selected.month,
            selected_date=selected,
            callback_prefix="element_date_",
            callback_suffix=f'_{_element_id}',
            first_date=old_date.date()
        )
    )
    await callback.answer()


async def handle_callback_element_date_prev(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, _, y, m, _element_id = callback.data.split("_")
    current = date(int(y), int(m), 1)
    prev_month = (current.replace(day=1) - timedelta(days=1)).replace(day=1)

    if not await validate_state(callback, state, _element_id, True):
        return
    data = await state.get_data()
    selected = date.fromisoformat(data['selected_date']) if data.get('selected_date') else None
    old_date = datetime.fromisoformat(data['old_datetime']).astimezone(settings.DEFAULT_TZ)

    bid_date_str = old_date.strftime('%d.%m.%Y')
    bid_selected_date_str = selected.strftime('%d.%m.%Y') if selected else ''
    msg_txt = TXT_ELEMENT_EDIT_DATE(_element_id, bid_date_str, bid_selected_date_str)

    await callback.message.edit_text(
        text=msg_txt,
        reply_markup=inline_calendar_keyboard(
            calendar_year=prev_month.year,
            calendar_month=prev_month.month,
            selected_date=selected,
            callback_prefix="element_date_",
            callback_suffix=f'_{_element_id}',
            first_date=old_date.date()
        )
    )
    await callback.answer()


async def handle_callback_element_date_next(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, _, y, m, _element_id = callback.data.split("_")
    current = date(int(y), int(m), 1)
    next_month = (current.replace(day=28) + timedelta(days=4)).replace(day=1)

    if not await validate_state(callback, state, _element_id, True):
        return

    data = await state.get_data()
    selected = date.fromisoformat(data['selected_date']) if data.get('selected_date') else None
    old_date = datetime.fromisoformat(data['old_datetime']).astimezone(settings.DEFAULT_TZ)

    bid_date_str = old_date.strftime('%d.%m.%Y')
    bid_selected_date_str = selected.strftime('%d.%m.%Y') if selected else ''
    msg_txt = TXT_ELEMENT_EDIT_DATE(_element_id, bid_date_str, bid_selected_date_str)

    await callback.message.edit_text(
        text=msg_txt,
        reply_markup=inline_calendar_keyboard(
            calendar_year=next_month.year,
            calendar_month=next_month.month,
            selected_date=selected,
            callback_prefix="element_date_",
            callback_suffix=f'_{_element_id}',
            first_date=old_date.date()
        )
    )
    await callback.answer()


async def handle_callback_element_date_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, _, _element_id = callback.data.split('_')
    if not await validate_state(callback, state, _element_id, True):
        return
    await state.clear()
    await callback.message.edit_text('Действие отменено')

async def handle_callback_element_date_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    selected_date = datetime.fromisoformat(data["selected_date"]).date()
    old_datetime = datetime.fromisoformat(data['old_datetime']).astimezone(settings.DEFAULT_TZ)

    new_datetime = datetime(
        year=selected_date.year,
        month=selected_date.month,
        day=selected_date.day,
        hour=old_datetime.hour,
        minute=old_datetime.minute,
        tzinfo=settings.DEFAULT_TZ
    )

    await state.update_data(new_datetime=new_datetime.isoformat())

    msg_txt = (f'📍 Прежняя дата: <b>{old_datetime.strftime('%d.%m.%Y')}</b>\n'
               f'➡️ Новая дата: <u><b>{new_datetime.strftime('%d.%m.%Y')}</b></u>')
    await callback.message.edit_text(msg_txt, reply_markup=None)
