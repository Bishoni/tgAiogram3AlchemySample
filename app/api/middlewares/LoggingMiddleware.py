import logging
import time
import json
from starlette.types import ASGIApp, Scope, Receive, Send, Message

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        start_time = time.time()
        path = scope.get("path", "-")
        method = scope.get("method", "-")
        client = scope.get("client", ("-",))[0]

        body_chunks = []

        async def send_wrapper(message: Message) -> None:
            nonlocal body_chunks
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                logger.info(f"{client} - {method} {path} → {message['status']} ({process_time:.2f}s)")
            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    body_chunks.append(body)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            if body_chunks:
                full_body = b"".join(body_chunks)
                try:
                    json_body = json.loads(full_body)
                    compact = json.dumps(json_body, ensure_ascii=False, separators=(",", ":"))
                    logger.info(f"Response body for {method} {path}: {compact}")
                except Exception:
                    logger.debug(f"Raw response body for {method} {path} (non-JSON): {full_body!r}")
