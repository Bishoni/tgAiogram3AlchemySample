# Шаблон Telegram бота на Aiogram 3 + SQLAlchemy

Данный проект представляет собой комплексный шаблон для разработки масштабируемых Telegram ботов с использованием фреймворка **Aiogram 3**, ORM **SQLAlchemy** (с использованием asyncpg) для работы с базой данных и **Alembic** для управления миграциями. Проект реализован с учётом принципов модульности и разделения ответственности, что позволяет легко расширять функциональность и поддерживать кодовую базу.

## Технологический стек

- **Telegram API:** Aiogram 3
- **ORM:** SQLAlchemy (asyncpg)
- **База данных:** PostgreSQL
- **Миграции:** Alembic
- **Логирование:** logging

## Архитектура проекта

Проект структурирован по принципу мини-сервисов. Каждый модуль бота организован в виде самостоятельного сервиса с собственной логикой, DAO, роутерами и утилитами. Это обеспечивает высокую модульность, удобство масштабирования и поддержки.

### Структура проекта

```
├── Dockerfile
├── README.md
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── actions
│   │   ├── __init__.py
│   │   ├── services
│   │   │   └── __init__.py
│   │   └── shared
│   │       ├── __init__.py
│   │       └── utils.py
│   ├── bot
│   │   ├── __init__.py
│   │   ├── create_bot.py
│   │   └── management
│   │       ├── __init__.py
│   │       ├── admin
│   │       ├── __init__.py
│   │       ├── dao
│   │       │   ├── __init__.py
│   │       │   └── dao.py
│   │       ├── filters
│   │       │   ├── __init__.py
│   │       │   └── filters.py
│   │       ├── middlewares
│   │       │   └── __init__.py
│   │       ├── router.py
│   │       ├── services
│   │       │   ├── __init__.py
│   │       └── utils
│   │           ├── __init__.py
│   │           └── utils.py
│   ├── shared
│   │   ├── __init__.py
│   │   ├── dao
│   │   │   ├── __init__.py
│   │   │   └── dao.py
│   │   ├── filters
│   │   │   ├── __init__.py
│   │   │   └── filters.py
│   │   ├── keyboards
│   │   │   ├── __init__.py
│   │   │   ├── inline.py
│   │   │   └── keyboard.py
│   │   ├── middlewares
│   │   │   ├── __init__.py
│   │   │   ├── errors.py
│   │   │   ├── log.py
│   │   │   ├── only_private_chat.py
│   │   │   └── throttling.py
│   │   ├── router.py
│   │   ├── services
│   │   │   └── __init__.py
│   │   └── utils
│   │       ├── __init__.py
│   │       └── utils.py
│   └── user
│       ├── __init__.py
│       ├── dao
│       │   └── __init__.py
│       ├── filters
│       │   └── __init__.py
│       ├── middlewares
│       │   └── __init__.py
│       ├── router.py
│       ├── services
│       │   ├── __init__.py
│       │   └── start
│       │       ├── __init__.py
│       │       ├── handler.py
│       │       ├── keyboards
│       │       │   ├── __init__.py
│       │       │   ├── inline.py
│       │       │   └── keyboard.py
│       │       ├── main.py
│       │       ├── state.py
│       │       └── utils.py
│       └── utils
│           ├── __init__.py
│           └── utils.py
├── config
│   ├── __init__.py
│   └── settings.py
├── dto
│   ├── Models
│   │   ├── Admin
│   │   │   ├── SAdmin.py
│   │   │   ├── SAdminCreate.py
│   │   │   ├── SAdminUpdate.py
│   │   │   ├── _AdminBase.py
│   │   │   └── __init__.py
│   │   ├── User
│   │   │   ├── SUser.py
│   │   │   ├── SUserCreate.py
│   │   │   ├── SUserUpdate.py
│   │   │   ├── _UserBase.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
├── extra
│   └── media
├── log
│   ├── __init__.py
│   ├── custom_logger.py
│   └── logs
│       └── log.txt
├── main_dao
│   ├── __init__.py
│   ├── base.py
│   ├── database.py
│   ├── database_middleware.py
│   ├── migration
│   │   ├── README
│   │   ├── __init__.py
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── __init__.py
│   │       └── fe9032ec83c5_init.py
│   └── models.py
├── run.py
└── scheduler
│   ├── __init__.py
│   ├── add_default_jobs.py
│   └── create_scheduler.py
├── docker-compose.yml
└── requirements.txt
```

### Компоненты мини-сервиса

Каждый мини-сервис имеет следующую структуру:

- **[actions](app/actions)** — содержит вспомогательные сервисы, отвечающие за реализацию специализированной логики, не связанной напрямую с Telegram-ботом. В том числе — [services](app/actions/services) для модульной обработки задач, выходящих за рамки стандартных взаимодействий пользователя с ботом.

- **[bot](app/bot)** — основной компонент Telegram-бота.  
  Включает:
  - [create_bot.py](app/bot/create_bot.py) — инициализация бота.
  - [management](app/bot/management) — логика управления, разделённая на:
    - [admin](app/bot/management/admin) — административная часть;
    - [user](app/bot/management/user) — пользовательская часть.
    - [shared](app/bot/management/shared) — общее для обоих: [middlewares](app/bot/management/shared/middlewares) и [services](app/bot/management/shared/services).

  Для реализации сервисов есть шаблон:
  - [handler.py](app/bot/management/user/services/start/handler.py) — обработка входящих Telegram-сообщений;
  - [main.py](app/bot/management/user/services/start/main.py) — регистрация хендлеров;
  - [keyboards](app/bot/management/user/services/start/keyboards) — inline и reply-клавиатуры;
  - [state.py](app/bot/management/user/services/start/state.py) — состояния FSM;
  - [utils.py](app/bot/management/user/services/start/utils.py) — вспомогательные функции (при усложнении логики — выносится в `actions`).

- **[config](app/config)** — конфигурация проекта.  
  Основной файл — [settings.py](app/config/settings.py): описывает константы и импортирует переменные окружения из [.env](.env).

- **[dto](app/dto)** — Data Transfer Object.  
  В папке [Models](app/dto/Models) определены структуры для создания и обновления моделей базы данных. Используются для обмена данными между слоями приложения. По большей части ведется создание/изменения записей в БД через это.

- **[extra](app/extra)** — содержит вспомогательные ресурсы проекта.  
  Папка [media](app/extra/media) используется для хранения медиафайлов и указывается по умолчанию в конфигурации.

- **[log](app/log)** — настройка логирования.  
  Используется модуль `logging`, в том числе `get_logger(__name__)`. Логи также записываются в файлы в папке [logs](app/log/logs).

- **[main_dao](app/main_dao)** — реализация DAO-уровня и абстракция работы с базой данных.  
  Включает модели, сессии и миграции. Подробнее о работе с классом будет ниже.

- **[scheduler](app/scheduler)** — модуль планировщика задач.  
  Используется для запуска периодических заданий и настройки дефолтных джобов.

- **[Dockerfile](Dockerfile) и [docker-compose.yml](docker-compose.yml)** – докер файлы для развертки проекта через docker. Обязательно прокидывать папки [logs](app/log/logs) и [media](app/extra/media) с хоста!

## Конфигурация

### Переменные окружения
 ```env
 BOT_TOKEN="999999:ffffffffff"
 POSTGRESQL_URL="postgresql+asyncpg://login:pass@0.0.0.0:5432/database"
 REDIS_URL="redis://log:pass@0.0.0.0:6379/number_db"
 ```
 - **BOT_TOKEN**: Токен Telegram-бота, выданный через [BotFather](https://t.me/BotFather).
 - **POSTGRESQL_URL**: Строка подключения к базе данных PostgreSQL.
 - **REDIS_URL**: Строка подключения к Redis.

### Зависимости

```
pydantic==2.10.6  # При повышении версии смотреть совместимость с aiogram
SQLAlchemy==2.0.40
aiogram==3.19.0  # При добавлении aiogram-dialog смотреть совместимость
APScheduler==3.11.0
pydantic-settings==2.8.1
asyncpg==0.30.0
pytz==2025.2
alembic==1.15.2
redis==5.2.1
greenlet==3.1.1
cachetools==5.5.2
```

## Управление базой данных

### Конфигурация базовой модели

В проекте используется базовая модель SQLAlchemy с общими полями:

```python
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self, exclude_none: bool = False):
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, uuid.UUID):
                value = str(value)

            if not exclude_none or value is not None:
                result[column.key] = value

        return result
```

### Объекты доступа к данным (DAO)

Проект реализует базовый класс BaseDAO с общими операциями базы данных:

- `find_one_or_none_by_id` — поиск записи по ID.
- `find_one_or_none` — поиск одной записи, удовлетворяющей заданным фильтрам.
- `find_all` — поиск всех записей, удовлетворяющих заданным фильтрам (при отсутствии фильтров возвращает все записи).
- `add` — добавление новой записи.
- `add_many` — добавление нескольких записей одновременно.
- `update` — обновление записей, удовлетворяющих указанному фильтру, с заданными новыми значениями.
- `delete` — удаление записей, удовлетворяющих указанному фильтру.
- `count` — подсчет количества записей, удовлетворяющих заданным фильтрам.
- `bulk_update` — массовое обновление записей по списку данных (обновление происходит для каждой записи по её ID).

Сервис-специфичные DAO наследуются от BaseDAO:

```python
from app.main_dao.base import BaseDAO
from app.main_dao.models import TgUser

class UserDAO(BaseDAO[TgUser]):
    model = TgUser
```

Пример использования:
```python
### Пример обработки команды `/start` с использованием `UserDAO` и `AdminDAO`

async def handle_start_command(message: Message, session: AsyncSession, state: FSMContext):
    await state.clear()

    user_data = message.from_user
    user_id = user_data.id

    user_dao = UserDAO(session)
    admin_dao = AdminDAO(session)
    user_info = await user_dao.find_by_telegram_id(user_id)   # Дополнительно определенный метод для UserDAO и AdminDAO

    MSG_TXT = f"Здравствуйте, <i><b>{user_data.first_name}</b></i>!"

    if user_info is None:
        # Создание пользователя, если он не найден в БД
        user_create = SUserCreate(
            telegram_id=user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            is_premium=user_data.is_premium
        )
        await user_dao.add(user_create)
        await session.flush()

        admin_create = SAdminCreate(telegram_id=user_id)
        await admin_dao.add(admin_create)
    else:
        # Обновление пользователя, если он найден в БД
        user_update = SUserUpdate(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            is_premium=user_data.is_premium
        )
        await user_dao.update(filters=SUser(telegram_id=user_id), values=user_update)

    await message.answer(MSG_TXT, reply_markup=inline_success_click())
    await message.delete()
```

## Порядок миграции базы данных

1. Определить модели в файле [models.py](app/main_dao/models.py)
2. Импортировать модели в [env.py](app/main_dao/migration/env.py)
3. Сгенерируйте текущую схему базы данных как соответствующую последней миграции:
   ```bash
   alembic stamp head
   ```
4. Создайте новую миграцию (автоматическое сравнение текущей модели с состоянием базы данных):
   ```bash
   alembic revision --autogenerate -m "Комментарий на английском языке"
   ```
5. Проверьте внимательно миграцию, созданную в папке [versions](app/main_dao/migration/versions). Если в файле присутствуют последовательности или другие необходимые данные, внесите их, уделяя особое внимание корректности синтаксиса. Alembic автоматически генерирует миграции поверхностно, поэтому итоговый код требует ручной проверки.   
   Например, в начале функции `def upgrade() -> None:` для генерации последовательности укажите
   ```Alembik
   op.execute("CREATE SEQUENCE IF NOT EXISTS tg_user_id_seq")
   ```
   
   Но после этого обязательно укажите в `def downgrade() -> None:` дроп последовательности:
   ```Alembik
   op.execute("DROP SEQUENCE IF EXISTS tg_user_id_seq")
   ```
   
6. Предварительно убедитесь, что в [.env](.env) указана верная строка подключения к БД, и указанная в ней база данных предварительно существует.
   
7. Примените миграцию к базе данных.
8. ```bash
   alembic upgrade head
   ```

## Лучшие практики

1. **Строить модули как отдельные сервисы**  
   Каждый компонент должен быть изолирован и отвечать только за свою область ответственности.
2. **Использовать `BaseDAO`**  
   Это обеспечивает единообразие и переиспользуемость при работе с базой данных.
3. **Соблюдать архитектурную структуру проекта**  
   При добавлении новых функций следовать принятой модульной организации.
4. **Вносить изменения в схему базы только через Alembic**  
   Это гарантирует контроль и версионирование изменений.

## В случае возникновения вопросов

- В кодовой базе приведены подробные примеры реализации различных функциональностей, которые помогут разобраться в особенностях работы проекта. Если возникнут дополнительные вопросы, можете обращаться
- Telegram: [@elite_pizza](https://t.me/elite_pizza)
---

Этот шаблон предоставляет надежную основу для создания масштабируемых и поддерживаемых Telegram ботов с использованием Aiogram 3 и SQLAlchemy.
