from fastapi import FastAPI
from api.controller import auth_controller
from api.core.database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth_controller.router)
