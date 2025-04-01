from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Union
import asyncio
import logging
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: Union[int, float] = 1.0):
        self.rate_limit = rate_limit
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if user_id in self.cache:
            bot: Bot = data['bot']
            if isinstance(event, Message):
                await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
                msg = await bot.send_message(
                    chat_id=event.chat.id,
                    text="<b><i>Пожалуйста, немного подождите перед следующей отправкой сообщения</i></b>"
                )
                logger.warning(f"Частая отправка сообщений от {event.from_user.id}")
                await asyncio.sleep(self.rate_limit)
                await msg.delete()
            elif isinstance(event, CallbackQuery):
                await event.answer("Пожалуйста, немного подождите перед следующим действием", show_alert=True)
                logger.warning(f"Частое нажатие на callback-кнопки от {event.from_user.id}")
            return
        self.cache[user_id] = True
        return await handler(event, data)