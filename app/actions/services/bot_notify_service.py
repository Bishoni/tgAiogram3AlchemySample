import logging

from app.actions.shared.wraps.wrap_telegram_error_handler import wrap_telegram_error_handler
from app.api.docs.Enums.app_response_codes import AppResponseCode
from app.api.docs.Enums.http_status import HttpStatusCode
from app.api.schemas.response import ResponseFromAnotherLogic
from app.bot.create_bot import bot

logger = logging.getLogger(__name__)


@wrap_telegram_error_handler
async def notify_user_by_bot(user_id: int, text: str) -> ResponseFromAnotherLogic:
    await bot.send_message(chat_id=user_id, text=text)
    return ResponseFromAnotherLogic(message="Сообщение успешно отправлено", http_status=HttpStatusCode.OK, code=AppResponseCode.TG_200)
