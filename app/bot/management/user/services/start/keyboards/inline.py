from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_main_start() -> InlineKeyboardMarkup:
    inline_kb_list = [
        [InlineKeyboardButton(text='Календарь', callback_data='calendar')],
        [InlineKeyboardButton(text='Закрыть сообщение', callback_data='close_message')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
