from aiogram import Router
from app.bot.management.user.services.start.handler import register_handlers as reg_start

router = Router(name='user')


def register_user_handlers():
    reg_start(router)
