from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import TypedDict


class DictGenerateCallback(TypedDict):
    cb_title: str
    cb_data: str


def inline_one_button(signature: str, callback_data: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с одной inline-кнопкой.

    :param signature: Текст кнопки.
    :param callback_data: Callback data для обработки нажатия.
    :return: InlineKeyboardMarkup с одной кнопкой.
    """
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=signature, callback_data=callback_data)]])


def inline_custom_buttons(buttons_dict: dict) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с набором inline-кнопок на основе словаря.

    :param buttons_dict: Словарь, где ключ — текст кнопки, значение — callback_data.
    :return: InlineKeyboardMarkup с кнопками, расположенными по одной в строке.
    """
    inline_kb_list = [
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
        for text, callback_data in buttons_dict.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def inline_paginated_keyboard(items: list[DictGenerateCallback], current_page: int, callback_prefix_page: str,
                              items_per_page: int = 10, extra_top_buttons: list[DictGenerateCallback] = None,
                              extra_bottom_buttons: list[DictGenerateCallback] = None) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с пагинацией для списка items.\n
    Все кнопки передаются в формате: [{'cb_title': 'Название', 'cb_data': 'Данные'}, ...]

    :param items: Список словарей основных кнопок.
    :param current_page: Текущая страница.
    :param callback_prefix_page: Префикс для перелистывания страниц.
    :param items_per_page: Суммарное количество вертикальных элементов на страницу.
    :param extra_top_buttons: Список словарей дополнительных верхних кнопок.
    :param extra_bottom_buttons: Список словарей дополнительных нижних кнопок.
    """
    builder = InlineKeyboardBuilder()
    total = len(items)
    extra_top_buttons = extra_top_buttons or []
    extra_bottom_buttons = extra_bottom_buttons or []

    max_items = max(items_per_page - len(extra_top_buttons) - 1, 1)
    if total == 0:
        for item in extra_top_buttons:
            builder.row(InlineKeyboardButton(text=item['cb_title'], callback_data=item['cb_data']))
        for item in extra_bottom_buttons:
            builder.row(InlineKeyboardButton(text=item['cb_title'], callback_data=item['cb_data']))
        return builder.as_markup()

    total_pages = (total + max_items - 1) // max_items
    start = (current_page - 1) * max_items
    end = start + max_items

    for item in extra_top_buttons:
        builder.row(InlineKeyboardButton(text=item['cb_title'], callback_data=item['cb_data']))

    for item in items[start:end]:
        builder.button(text=item['cb_title'], callback_data=item['cb_data'])
    builder.adjust(1)

    nav = []
    if current_page > 1:
        nav.append(InlineKeyboardButton(text='<-', callback_data=f"{callback_prefix_page}{current_page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data=f'noop_{current_page}'))
    if current_page < total_pages:
        nav.append(InlineKeyboardButton(text='->', callback_data=f"{callback_prefix_page}{current_page + 1}"))
    builder.row(*nav)

    for item in extra_bottom_buttons:
        builder.row(InlineKeyboardButton(text=item['cb_title'], callback_data=item['cb_data']))

    return builder.as_markup()


def inline_close_message():
    inline_kb_list = [
        [InlineKeyboardButton(text='Назад', callback_data='close_message')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list )