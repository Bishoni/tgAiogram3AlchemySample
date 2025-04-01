import asyncio
import logging
import re
from datetime import datetime
import itertools

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config.settings import settings

logger = logging.getLogger(__name__)


def log_shared_action(user, action):
    logger.info(f'\nОбщий пользователь ID: ({user.id}); username: (@{user.username}); first_name: ({user.first_name}) сделал запрос: \n{action}')


SQL_INJECTION_PATTERN = re.compile(r"'|--|(/\*(?:.|[\r\n])*?\*/)|\b(?:select|insert|update|delete|drop|alter|union|create|rename)\b", re.IGNORECASE)
def sanitize_text(text: str) -> str:
    """
    Функция очищает текст от HTML-тегов и типичных конструкций, используемых для SQL-инъекций.

    Параметры:
      text (str): исходный текст для очистки.

    Возвращает:
      str: очищенный текст.
    """
    cleaned_text = text
    if isinstance(text, str):
        text = text.replace("<", "").replace(">", "").strip()
        cleaned_text = re.sub(SQL_INJECTION_PATTERN, '', text)
    return cleaned_text


def generate_dynamic_lines(text: str) -> str:
    """
    Формирует текст с динамической разделительной линией в зависимости от длины очищенного текста.

    Args:
        text (str): Исходный текст.

    Returns:
        str: Оригинальный текст и строка из символов '➖', длина которой зависит от длины очищенного текста.
    """
    cleaned = sanitize_text(text)
    length = len(cleaned)
    min_symbols, max_symbols = 2, 6   # Минимум 2, максимум 6
    count = max(min_symbols, min(max_symbols, length // 5))
    separator = '➖' * count
    return f"{text}\n{separator}"


def format_datetime_in_default_timezone(dt: datetime | None) -> str:
    """
    Форматирует объект datetime в строку в часовом поясе приложения (DEFAULT_TIMEZONE).

    Args:
        dt (datetime | None): Дата и время для форматирования.

    Returns:
        str: Отформатированная дата-время в формате 'DD.MM.YYYY HH:MM TZ' или 'Нет', если dt is None.
    """
    if dt is None:
        return "Нет"
    tz = settings.DEFAULT_TZ
    dt_converted = dt.astimezone(tz)
    return f"{dt_converted.strftime('%d.%m.%Y %H:%M')} {settings.DEFAULT_TZ_ABBR}"


def get_current_time_in_default_timezone():
    """
    Возвращает текущую дату и время в часовом поясе по умолчанию приложения в виде форматированной строки.

    Возвращает:
        str: Отформатированная дата-время в формате 'DD.MM.YYYY HH:MM TZ', где TZ – часовой пояс приложения по умолчанию
    """
    tz = settings.DEFAULT_TZ
    dt_converted = datetime.now(tz)
    return f"{dt_converted.strftime('%d.%m.%Y %H:%M')} {settings.DEFAULT_TZ_ABBR}"


async def animate_waiting_message(event: CallbackQuery | Message, signature: str = 'Подготавливаю ответ', interval: float = 0.8,
                                  max_cycles: int | None = None, finish_text: str | None = None) -> None:
    """
    Показывает анимированное сообщение ожидания с циклическими эмодзи и точками.
    Возвращает финальное сообщение или удаляет его.

    Args:
        event (CallbackQuery | Message): Объект для ответа.
        signature (str): Базовый текст без эмодзи и точек.
        interval (float): Интервал обновления в секундах.
        max_cycles (int | None): Максимальное число циклов анимации.
        finish_text (str | None): Текст, который заменит сообщение по завершении, если указан.
    """
    emojis = itertools.cycle("🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚")
    dots = itertools.cycle(["", ".", "..", "..."])
    send_method = event.message.answer if isinstance(event, CallbackQuery) else event.answer
    message = await send_method(text=f"{next(emojis)} <b>{signature}</b>", disable_web_page_preview=True)

    cycle = 0
    try:
        while max_cycles is None or cycle < max_cycles:
            await asyncio.sleep(interval)
            try:
                await message.edit_text(f"{next(emojis)} <b>{signature}{next(dots)}</b>")
            except TelegramBadRequest:
                pass
            cycle += 1
    finally:
        if finish_text:
            try:
                await message.edit_text(finish_text)
            except TelegramBadRequest:
                await message.delete()
        else:
            await message.delete()


def split_long_message(text: str, max_length: int = 4000) -> list[str]:
    """
    Разбивает длинный текст на части, не превышающие max_length символов.
    Сохраняет целостность строк и слов, разбивая сначала по переносу строки, затем по пробелам в ней.

    Args:
        text: Исходный текст для разбивки.
        max_length: Максимальная длина каждой части.

    Returns:
        list[str]: Список частей текста.
    """
    if len(text) <= max_length:
        return [text]

    parts: list[str] = []
    index = 0
    length = len(text)

    while index < length:
        end = min(index + max_length, length)
        segment = text[index:end]

        # Пытается найти лучший разрыв: сначала по новой строке, затем по пробелу
        if end < length:
            newline_pos = segment.rfind('\n')
            space_pos = segment.rfind(' ')
            split_pos = newline_pos if newline_pos != -1 else space_pos

            if split_pos > 0:
                end = index + split_pos + 1

        part = text[index:end].rstrip()
        parts.append(part)
        index = end

    return parts


async def delete_messages_from_state(state: FSMContext, event: CallbackQuery | Message) -> None:
    """
    Асинхронно удаляет сообщения, идентификаторы которых хранятся в состоянии FSM под ключом 'message_ids'.
    После попыток удаления всех сообщений, функция сбрасывает значение 'message_ids' в состоянии до пустого списка.
    """
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    if message_ids:
        for msg_id in message_ids:
            try:
                await event.bot.delete_message(chat_id=event.from_user.id, message_id=msg_id)
                await asyncio.sleep(0.1)
            except (TelegramBadRequest, AttributeError):  # AttributeError: 'InaccessibleMessage' object has no attribute 'delete'
                pass
        await state.update_data(message_ids=[])