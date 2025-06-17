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
        status_code = None

        async def send_wrapper(message: Message) -> None:
            nonlocal body_chunks, status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    body_chunks.append(body)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            process_time = time.time() - start_time
            full_body = b"".join(body_chunks)
            request_id = "N/A"
            status = "unknown"

            if full_body:
                try:
                    json_body = json.loads(full_body)
                    request_id = json_body.get("meta", {}).get("request_id", "N/A")
                    status = json_body.get("meta", {}).get("status", "unknown").lower()
                    compact = json.dumps(json_body, ensure_ascii=False, separators=(",", ":"))
                    log_msg = (
                        f"[{status.upper()}] {client} - {method} {path} → {status_code} "
                        f"({process_time:.2f}s), request_id: {request_id}"
                    )
                    if status == "error":
                        logger.warning(log_msg + f"\nJSON-response: {compact}")
                    else:
                        logger.info(log_msg)
                        pass
                except Exception:
                    logger.warning(
                        f"[RAW] {client} - {method} {path} → {status_code} ({process_time:.2f}s), "
                        f"raw: {full_body!r}, request_id: {request_id}"
                    )
            else:
                logger.info(
                    f"[EMPTY] {client} - {method} {path} → {status_code} ({process_time:.2f}s), "
                    f"request_id: {request_id}"
                )
