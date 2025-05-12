import asyncio
import locale

from app.bot.create_bot import dp, bot, admin_router, user_router, shared_router
from app.scheduler.create_scheduler import scheduler
from app.scheduler.add_default_jobs import add_default_jobs
from app.log.custom_logger import setup_logging
import logging
from uvicorn import Config, Server

logger = logging.getLogger(__name__)



async def setup_api():
    root_logger = logging.getLogger()
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "asyncio"]:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = False
        for handler in root_logger.handlers:
            logger.addHandler(handler)
        logger.setLevel(root_logger.level)

    config = Config(
        "app.api.v1.main:app",
        host="0.0.0.0",
        port=35921,
        log_level="info",
        loop="asyncio",
        log_config=None
    )
    server = Server(config)
    asyncio.create_task(server.serve())

def setup_routers():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(shared_router)


async def setup_scheduler():
    scheduler.start()
    await add_default_jobs()


async def main():
    setup_logging()
    setup_routers()
    await setup_scheduler()
    await setup_api()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.exception(f"Ошибка при запуске бота: \n{logger.critical('e')}")
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())