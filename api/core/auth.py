from datetime import timedelta
import datetime
import re
import jwt
from time import time, timezone
from datetime import datetime
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

from api.models.dto.user_dto import UserResponseDTO


load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE")


class Token(BaseModel):
    access_token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def token_response(token: str) -> dict:
    return {"token": token}


def sign(user_data: UserResponseDTO) -> str:
    payload = {
        "email": user_data.email,
        "username": user_data.username,
        "role": user_data.role,
        "exp": time() + 3600,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["exp"] >= time() else None

    except:
        return {}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)
