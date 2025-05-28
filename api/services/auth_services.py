from typing import ValuesView
from api.core import auth
from sqlalchemy.orm import Session
from api.repository import user_repository as repository
from api.models.user import User
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO


def register_user(user: UserCreateDTO, db: Session):
    existing = repository.get_user_by_email(db, user.email)
    if existing:
        raise ValueError("User already exists with this email!")

    if user.password != user.confirm_password:
        raise ValueError("Password need be the same!")

    user = User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password),
    )
    return repository.create_user(db, user)


def login(user_login: UserLoginDTO, db: Session):
    user_data = repository.get_user_by_email(db, user_login.email)
    if not user_data:
        raise ValueError("Email not found!")

    if not auth.verify_password(user_login.password, user_data.password):
        raise ValueError("Invalid Password!")

    return auth.sign(user_data.username, user_data.email)


def get_all(db: Session):
    return repository.find_all(db)
