from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
import asyncio
import traceback
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.critical(f"При обработке действия пользователя возникла ошибка: {e} \n{traceback.format_exc()}")
            text_notify = "⚠️ Произошла ошибка при обработке вашего запроса.\nОтладочная информация была записана в лог!"
            if isinstance(event, Message):
                msg = await event.reply(text_notify)
                await asyncio.sleep(10)
                await msg.delete()
            elif isinstance(event, CallbackQuery):
                await event.answer(text_notify)
            return None
