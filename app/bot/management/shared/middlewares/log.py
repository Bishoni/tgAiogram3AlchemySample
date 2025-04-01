import logging
from inspect import unwrap

from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery, PollAnswer

logger = logging.getLogger(__name__)


class LogActionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        user, action_type = None, None
        if isinstance(event, Message):
            user = event.from_user
            action_type = 'Сообщение'
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            action_type = 'Кнопка'
        elif isinstance(event, PollAnswer):
            user = event.user
            action_type = 'Ответ в опросе'

        if user:
            unwrapped_func = unwrap(handler)
            try:
                real = unwrapped_func.__self__.callback
                action = real.__doc__ or f'Вызов функции: {real.__name__}'
            except Exception:
                action = f'Хендлер: {unwrapped_func}'

            router = data.get("event_router")
            router_name = router.name.lower() if router else ""
            if "admin" in router_name:
                prefix = "Администратор"
            elif "user" in router_name:
                prefix = "Пользователь"
            elif "shared" in router_name:
                prefix = "Общий"
            else:
                prefix = "Неизвестный"

            logger.info(f"\n[{prefix}] ID: ({user.id}); username: (@{user.username}); first_name: ({user.first_name}); route: ({router_name}); сделал запрос:\n({action_type}) {action}")
        return await handler(event, data)
