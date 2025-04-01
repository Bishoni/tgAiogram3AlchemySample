from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config.settings import settings

scheduler = AsyncIOScheduler(timezone=settings.DEFAULT_TZ)
