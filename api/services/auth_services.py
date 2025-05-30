from typing import ValuesView
from api.core import auth
from sqlalchemy.orm import Session
from api.execptions import user_exceptions
from api.models.dto.user_dto import UserCreateDTO
from api.repository import user_repository as repository
from api.models.user import User
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO


def register_user(user: UserCreateDTO, db: Session):
    existing = repository.get_user_by_email(db, user.email)
    if existing:
        raise user_exceptions.UserNotFound()

    user = User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password),
        role=user.role,
    )
    return repository.create_user(db, user)


def login(user_login: UserLoginDTO, db: Session):
    user_data = repository.get_user_by_email(db, user_login.email)
    if auth.verify_password(user_login.password, user_data.password):
        token = auth.sign(user_login.email)
        return user_data, token


def get_all(db: Session):
    return repository.find_all(db)
