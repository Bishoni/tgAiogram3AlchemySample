import os
import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    POSTGRESQL_URL: str = ""
    REDIS_URL: str = ""

    # Часовой пояс всего приложения и его аббревиатуры
    DEFAULT_TZ_NAME: ClassVar[str] = 'Europe/Moscow'
    DEFAULT_TZ_ABBR: ClassVar[str] = 'MSK'
    DEFAULT_TZ: ClassVar[pytz.BaseTzInfo] = pytz.timezone(DEFAULT_TZ_NAME)

    # Папка для всех медиа (находится: ../app/extra/media)
    MEDIA_DIR: ClassVar[str] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'extra', 'media'))

    # Загрузка переменных из конфига (.env, рядом с ../app)
    model_config = SettingsConfigDict(env_file=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env')))


settings = Settings()
