from fastapi import FastAPI, Request
from api.controller import auth_controller, whatsapp_controller
from api.core.log_conf import logger
from api.core.middleware import LogMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


app.add_middleware(LogMiddleware)
app.include_router(auth_controller.router)
app.include_router(whatsapp_controller.router)
