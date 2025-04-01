from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_success_click() -> InlineKeyboardMarkup:
    inline_kb_list = [
        [InlineKeyboardButton(text='Кнопка', callback_data='success_click')],
        [InlineKeyboardButton(text='Закрыть сообщение', callback_data='close_message')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
