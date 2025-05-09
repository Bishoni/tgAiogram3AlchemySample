import logging
import traceback
from typing import TypedDict
from aiogram.exceptions import (TelegramAPIError, TelegramRetryAfter, TelegramNotFound, TelegramForbiddenError,
                                TelegramBadRequest, TelegramServerError)
from app.bot.create_bot import bot

logger = logging.getLogger(__name__)


class BotNotifyResult(TypedDict):
    ok: bool
    message: str


async def notify_user_by_bot(user_id: int, text: str) -> BotNotifyResult:
    try:
        await bot.send_message(chat_id=user_id, text=text)
        return {"ok": True, "message": "Сообщение успешно отправлено"}

    except TelegramNotFound:
        msg = "Пользователь или чат не найден — возможно, пользователь не писал боту."
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}

    except TelegramForbiddenError:
        msg = "Бот заблокирован или удалён из чата."
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}

    except TelegramRetryAfter as e:
        msg = f"Превышен лимит запросов. Повтори через {e.retry_after} секунд."
        logger.warning(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}

    except TelegramBadRequest as e:
        if "chat not found" in str(e).lower():
            msg = "Чат не найден — пользователь не инициировал диалог с ботом."
        else:
            msg = f"Неверный запрос к Telegram API: {e}"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}

    except TelegramServerError as e:
        msg = f"Ошибка Telegram сервера (5xx): {e}"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}

    except TelegramAPIError as e:
        msg = f"Неизвестная ошибка Telegram API: {e}"
        logger.error(f"[{user_id}] {msg}\n{traceback.format_exc()}")
        return {"ok": False, "message": msg}
