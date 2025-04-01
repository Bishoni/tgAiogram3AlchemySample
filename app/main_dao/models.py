from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, BigInteger, Sequence, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.main_dao.database import Base


class TgUser(Base):
    """
    Pydantic-схема телеграмм-пользователя из базы данных.

    Attributes:
        id: Первичный ключ записи
        telegram_id: Телеграмм айди пользователя
        first_name: Имя пользователя
        last_name: Фамилия пользователя в Telegram
        username: Ссылка на пользователя в Telegram
        is_premium: Флаг премиум-подписки
        created_at: Дата создания записи в бд для пользователя
        updated_at: Дата последнего обновления записи в бд для пользователя
        registration_param: Метка регистрации телеграмм-пользователя
    """
    __tablename__ = 'tg_user'

    id: Mapped[int] = mapped_column(BigInteger, Sequence('tg_user_id_seq'), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    is_premium: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    registration_param: Mapped[str | None] = mapped_column(String, nullable=True)

    admin_account: Mapped["AdminAccount"] = relationship(
        "AdminAccount",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<TgUser(telegram_id={self.telegram_id}, first_name={self.first_name}, username={self.username})>"


class AdminAccount(Base):
    __tablename__ = 'admin_account'

    id: Mapped[int] = mapped_column(BigInteger, Sequence('admin_account_id_seq'), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('tg_user.telegram_id'), nullable=False, index=True)
    permission_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["TgUser"] = relationship(
        "TgUser",
        back_populates="admin_account",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<AdminAccount(telegram_id={self.telegram_id}, is_active={self.is_active}, permission_level={self.permission_level})>"
