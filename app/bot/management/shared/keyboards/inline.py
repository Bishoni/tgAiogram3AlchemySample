from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import TypedDict
from calendar import monthrange
from datetime import timedelta, date, datetime

from app.config.settings import settings


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
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def inline_calendar_keyboard(calendar_year: int,
                             calendar_month: int,
                             selected_date: date | None = None,
                             available_days_from_reference_date: int = 3,
                             available_days_before_reference_date: int = 1,
                             show_disabled: bool = False,
                             callback_prefix: str = "calendar_",
                             callback_suffix: str = '',
                             first_date: date | None = None) -> InlineKeyboardMarkup:
    """
    Создаёт inline-календарь с возможностью перехода назад и вперёд
    от заданной даты (или текущей) на заданное число дней.
    """

    if isinstance(first_date, datetime):
        first_date = first_date.date()
    if isinstance(selected_date, datetime):
        selected_date = selected_date.date()
    if isinstance(selected_date, str):
        selected_date = date.fromisoformat(selected_date)

    reference_date = first_date or datetime.now(tz=settings.DEFAULT_TZ).date()
    if selected_date is None:
        selected_date = reference_date

    first_available = reference_date - timedelta(days=available_days_before_reference_date)
    last_available = reference_date + timedelta(days=available_days_from_reference_date)

    weekday = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard: list[list[InlineKeyboardButton]] = []

    months_nominative = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = f"{months_nominative[calendar_month - 1]} {calendar_year}"

    # Пагинация
    has_prev = (calendar_year, calendar_month) > (first_available.year, first_available.month)
    has_next = (calendar_year, calendar_month) < (last_available.year, last_available.month)

    pagination_row = []
    if has_prev:
        pagination_row.append(InlineKeyboardButton(
            text="<<",
            callback_data=f"{callback_prefix}prev_{calendar_year}_{calendar_month}{callback_suffix}"
        ))
    if has_next:
        pagination_row.append(InlineKeyboardButton(
            text=">>",
            callback_data=f"{callback_prefix}next_{calendar_year}_{calendar_month}{callback_suffix}"
        ))
    if pagination_row:
        keyboard.append(pagination_row)

    keyboard.append([InlineKeyboardButton(text=month_name, callback_data="noop")])
    keyboard.append([InlineKeyboardButton(text=day, callback_data="noop") for day in weekday])

    first_day = date(calendar_year, calendar_month, 1)
    start_weekday = first_day.weekday()
    total_days = monthrange(calendar_year, calendar_month)[1]

    row: list[InlineKeyboardButton] = []

    for _ in range(start_weekday):
        row.append(InlineKeyboardButton(text=" ", callback_data="noop"))

    for day in range(1, total_days + 1):
        current = date(calendar_year, calendar_month, day)
        is_selected = selected_date == current

        if current < first_available or current > last_available:
            btn = InlineKeyboardButton(text=" ", callback_data="noop")
        else:
            text = f"[ {day} ]" if is_selected else str(day)
            btn = InlineKeyboardButton(
                text=text,
                callback_data=f"{callback_prefix}day_{calendar_year}_{calendar_month}_{day}{callback_suffix}"
            )
        row.append(btn)

        if len(row) == 7:
            if show_disabled or any(b.text.strip().isdigit() or "[" in b.text for b in row):
                keyboard.append(row)
            row = []

    if row:
        while len(row) < 7:
            row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
        if show_disabled or any(b.text.strip().isdigit() or "[" in b.text for b in row):
            keyboard.append(row)

    if selected_date:
        keyboard.append([
            InlineKeyboardButton(
                text="Подтвердить выбор даты",
                callback_data=f"{callback_prefix}confirm{callback_suffix}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="Отмена", callback_data=f"{callback_prefix}cancel{callback_suffix}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
