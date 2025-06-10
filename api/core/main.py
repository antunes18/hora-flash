from fastapi import FastAPI
from api.controller import auth_controller, whatsapp_controller, scheduling_controller
from api.core.middleware import LogMiddleware

app = FastAPI()


app.add_middleware(LogMiddleware)
app.include_router(auth_controller.router)
app.include_router(scheduling_controller.router)
app.include_router(whatsapp_controller.router)
