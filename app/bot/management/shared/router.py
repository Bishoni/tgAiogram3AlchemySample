from aiogram import Router
from app.bot.management.shared.services.main.handler import register_handlers as reg_main


router = Router(name='shared')

def register_shared_handlers():
    reg_main(router)
