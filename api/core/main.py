from fastapi import FastAPI
from api.controller import auth_controller, whatsapp_controller
from api.core.database import Base, engine


app = FastAPI()
app.include_router(auth_controller.router)

app.include_router(whatsapp_controller.router)
