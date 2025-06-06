from aiogram import Router
from app.bot.management.user.services.start.handler import register_handlers as reg_start
from app.bot.management.user.services.date_selection.handler import register_handlers as reg_date_selection

router = Router(name='user')


def register_user_handlers():
    reg_start(router)
    reg_date_selection(router)