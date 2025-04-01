import logging

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Message

logger = logging.getLogger(__name__)


class PrivateChatMiddleware(BaseMiddleware):

    def __init__(self, is_admin_router: bool = False):
        self.admin = is_admin_router

    async def __call__(self, handler, event, data):

        if isinstance(event, CallbackQuery):
            chat = event.message.chat
        else:
            chat = event.chat

        if chat.type == ChatType.PRIVATE:
            return await handler(event, data)

        logger.info(f'Неизвестное действие вне приватного чата. chat_id: {chat.id}')
        return None
