import time
import asyncio
import logging
from cachetools import TTLCache
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Union

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: Union[int, float] = 1.0):
        self.rate_limit = rate_limit
        self.cooldown_feedback = {}
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)
        self.last_activity_timestamps = {}

    async def __call__(self,
                       handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
                       event: Union[Message, CallbackQuery],
                       data: Dict[str, Any]
                       ) -> Any:
        user_id = event.from_user.id

        if user_id in self.cache:
            if user_id not in self.cooldown_feedback:
                bot: Bot = data['bot']
                await self._send_throttle_message(bot, event, user_id)
            elif isinstance(event, Message):
                await event.delete()
            return

        self.last_activity_timestamps[user_id] = time.time()
        self.cache[user_id] = True
        return await handler(event, data)

    async def _send_throttle_message(self, bot: Bot, event: Union[Message, CallbackQuery], user_id: int):
        if isinstance(event, Message):
            logger.warning(f"Пользователь {user_id} отправляет сообщения слишком часто")
            cooldown_msg = await bot.send_message(
                chat_id=event.chat.id,
                text=f"<b><i>Пожалуйста, подождите {int(self.get_remaining_ttl(user_id))} секунд...</i></b>")
            self.cooldown_feedback[user_id] = cooldown_msg
            self._run_cooldown_feedback_loop(bot, event, user_id, cooldown_msg)

        elif isinstance(event, CallbackQuery):
            logger.warning(f"Пользователь {user_id} нажимает кнопки слишком часто")
            await event.answer(f"Пожалуйста, подождите {int(self.get_remaining_ttl(user_id))} секунд...",
                               show_alert=True)

    def _run_cooldown_feedback_loop(self, bot: Bot, event: Message, user_id: int, message: Message):
        asyncio.create_task(self._update_cooldown_message(bot, event, user_id, message))

    async def _update_cooldown_message(self, bot: Bot, event: Message, user_id: int, message: Message):
        try:
            while True:
                remaining = self.get_remaining_ttl(user_id)
                if remaining <= 1.5:
                    break
                try:
                    await message.edit_text(f"<b><i>Пожалуйста, подождите {int(remaining)} секунд...</i></b>")
                except Exception as e:
                    logger.warning(f"Ошибка изменения сообщения: {e}")
                await asyncio.sleep(min(remaining, 5))
        finally:
            self.cooldown_feedback.pop(user_id, None)
            self.last_activity_timestamps.pop(user_id, None)
            await message.delete()

            recovery_msg = await bot.send_message(chat_id=event.chat.id,
                                                  text=f"<b><i>Теперь Вы можете повторно отправить сообщение</i></b>")
            await asyncio.sleep(self.rate_limit)
            await recovery_msg.delete()

    def get_remaining_ttl(self, user_id: int) -> float:
        added_at = self.last_activity_timestamps.get(user_id)
        if added_at is None:
            return 0
        elapsed = time.time() - added_at
        remaining = self.rate_limit - elapsed
        return max(0, remaining)
