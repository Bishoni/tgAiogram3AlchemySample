import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.management.user.services.date_selection.state import UserState
from app.config.settings import settings

logger = logging.getLogger(__name__)


TXT_ELEMENT_EDIT_DATE = lambda element_id, old_date, new_date: (
    f"Выберите новую дату для элемента №<code>{element_id}</code> \n\n"
    f"📍 Прежняя дата: <b>{old_date}</b> {settings.DEFAULT_TZ_ABBR}\n"
    f"➡️ Новая дата: <b><u>{new_date}</u></b> {settings.DEFAULT_TZ_ABBR}\n\n"
    f"Подтвердите действие соответствующей кнопкой!")


async def validate_state(callback: CallbackQuery, state: FSMContext, element_id_callback: str, send_callback: bool) -> bool:
    current_state = await state.get_state()
    if current_state and current_state.startswith(UserState.__name__):
        data = await state.get_data()
        element_id_state = data.get('element_id', '')
        if element_id_callback == element_id_state:
            if send_callback:
                await callback.answer()
            return True
    msg_txt = f'Пожалуйста, повторите взаимодействие с элементом №{element_id_callback}!'
    await callback.answer(msg_txt, show_alert=True)

    # reply_mk = inline_one_button("Профиль", "main_profile")
    reply_mk = None
    await callback.message.edit_text(msg_txt, reply_markup=reply_mk)
    return False
