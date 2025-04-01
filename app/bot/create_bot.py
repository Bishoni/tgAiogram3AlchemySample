from app.bot.management.admin.router import router as admin_router, register_admin_handlers
from app.bot.management.user.router import router as user_router, register_user_handlers
from app.bot.management.shared.router import router as shared_router, register_shared_handlers

from app.bot.management.shared.middlewares.errors import ErrorHandlingMiddleware
from app.bot.management.shared.middlewares.only_private_chat import PrivateChatMiddleware
from app.bot.management.shared.middlewares.throttling import ThrottlingMiddleware
from app.bot.management.shared.middlewares.log import LogActionMiddleware
from app.config.settings import settings

import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.main_dao.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit


async def set_commands():
    commands = [
        BotCommand(command="start", description="Обновить действия бота")
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()
    # logger.info('Бот запущен')


async def stop_bot():
    # logger.error('Бот остановлен')
    pass


logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# botStorage = MemoryStorage()
botStorage = RedisStorage.from_url(settings.REDIS_URL)
dp = Dispatcher(storage=RedisStorage.from_url(settings.REDIS_URL))

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)

dp.message.middleware(PrivateChatMiddleware())
dp.callback_query.middleware(PrivateChatMiddleware())

dp.message.middleware(ThrottlingMiddleware(1))
dp.callback_query.middleware(ThrottlingMiddleware(0.4))

dp.message.middleware(ErrorHandlingMiddleware())
dp.callback_query.middleware(ErrorHandlingMiddleware())

dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
dp.update.middleware.register(DatabaseMiddlewareWithCommit())

register_admin_handlers()
admin_router.message.middleware(LogActionMiddleware())
admin_router.callback_query.middleware(LogActionMiddleware())
admin_router.message.middleware(PrivateChatMiddleware(is_admin_router=True))
admin_router.callback_query.middleware(PrivateChatMiddleware(is_admin_router=True))

register_user_handlers()
user_router.message.middleware(LogActionMiddleware())
user_router.callback_query.middleware(LogActionMiddleware())

register_shared_handlers()
shared_router.message.middleware(LogActionMiddleware())
shared_router.callback_query.middleware(LogActionMiddleware())
