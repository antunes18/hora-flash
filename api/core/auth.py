import jwt
from time import time

from dotenv import load_dotenv
import os
from passlib.context import CryptContext


load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def token_response(token: str) -> dict:
    return {"access_token": token}


def sign(email: str) -> dict:
    payload = {"email": email, "exp": time() + 3600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token=token)


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
