import logging
import time
from starlette.types import ASGIApp, Scope, Receive, Send, Message

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            start_time = time.time()

            async def send_wrapper(message: Message) -> None:
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    logger.info(
                        f"{scope['method']} {scope['path']} → {message['status']} ({process_time:.2f}s)"
                    )
                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)