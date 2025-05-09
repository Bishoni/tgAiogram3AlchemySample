from fastapi import APIRouter
from app.api.v1.routes.ping import router as ping_router
from app.api.v1.routes.notify import router as notify_router

api_router = APIRouter()

api_router.include_router(ping_router, tags=["ping"])
api_router.include_router(notify_router, tags=["ping"])