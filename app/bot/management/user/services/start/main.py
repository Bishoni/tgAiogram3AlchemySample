from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.bot.management.user.services.start.keyboards.inline import inline_main_start
from app.dto.models.User.SUser import SUser
from app.dto.models.User.SUserCreate import SUserCreate
from app.dto.models.Admin.SAdminCreate import SAdminCreate
from app.dto.models.User.SUserUpdate import SUserUpdate
from app.bot.management.shared.dao.dao import UserDAO, AdminDAO


logger = logging.getLogger(__name__)


async def handle_start_command(message: Message, session: AsyncSession, state: FSMContext):
    """

    :param message:
    :param session:
    :param state:
    """
    await state.clear()

    user_data = message.from_user
    user_id = user_data.id

    user_dao = UserDAO(session)
    admin_dao = AdminDAO(session)
    user_info = await user_dao.find_by_telegram_id(user_id)

    MSG_TXT = 'Здравствуй'

    if user_info is None:
        user_create = SUserCreate(
            telegram_id=user_id,
            first_name=user_data.first_name,
            username=user_data.username,
            is_premium=user_data.is_premium,
            last_name=user_data.last_name
        )
        await user_dao.add(user_create)
        await session.flush()
        admin_create = SAdminCreate(telegram_id=user_id)
        await admin_dao.add(admin_create)
    else:
        user_update = SUserUpdate(
            first_name=user_data.first_name,
            username=user_data.username,
            is_premium=user_data.is_premium,
            last_name=user_data.last_name
        )
        await user_dao.update(filters=SUser(telegram_id=user_id), values=user_update)

    await message.answer(MSG_TXT, reply_markup=inline_main_start())
    await message.delete()
