from api.core.log_conf import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        log_dict = {
            "method": request.method,
            "url": str(request.url),
            "status": response.status_code,
            "response_body": response_body.decode("utf-8", errors="ignore"),
        }

        if response.status_code != 200 and 201:
            logger.error(log_dict)

        logger.info(log_dict)
        return response
