import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging

from app.bot.management.shared.utils.utils import delete_messages_from_state

logger = logging.getLogger(__name__)


async def handler_noop(callback: CallbackQuery, state: FSMContext):
    data_parts = callback.data.split('_')

    if len(data_parts) > 1:
        page = data_parts[1]
        msg_txt = f"Текущая страница:\n№{page}"
    else:
        msg_txt = "❕"

    await callback.answer(msg_txt, show_alert=True)


async def handler_close_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception as e:
        logger.info(f"Ошибка при удалении сообщения: {e}\n{traceback.format_exc()}")
    await delete_messages_from_state(state, callback)
