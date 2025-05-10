import logging

from app.actions.shared.telegram_error_handler import wrap_telegram_error_handler
from app.api.schemas.response import ResponseFromTelegramLogic
from app.bot.create_bot import bot

logger = logging.getLogger(__name__)


@wrap_telegram_error_handler
async def notify_user_by_bot(user_id: int, text: str) -> ResponseFromTelegramLogic:
    await bot.send_message(chat_id=user_id, text=text)
    return ResponseFromTelegramLogic(message="Сообщение успешно отправлено", http_status=200)
