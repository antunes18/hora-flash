from api.core import auth
from sqlalchemy.orm import Session
from api.exceptions import user_exceptions
from api.models.dto.user_dto import UserCreateDTO, UserResponseDTO, UserLoginDTO
from api.repository import user_repository as repository
from api.models.user import User
from api.core.auth import Token
from api.exceptions.user_exceptions import UserNotFound


def register_user(user: UserCreateDTO, db: Session):
    existing = repository.get_user_by_email(user.email, db)
    if existing:
        raise user_exceptions.UserAlreadyExist()

    user = User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password),
        role=user.role,
        disabled=False,
    )
    return repository.create_user(user, db)


def login(user_login: UserLoginDTO, db: Session) -> Token:
    user_data: UserResponseDTO = repository.get_user_by_email(user_login.email, db)

    if not user_data:
        raise user_exceptions.UserNotFound()

    if auth.verify_password(user_login.password, user_data.password):
        token = auth.sign(user_data)

        return Token(access_token=token)

    raise user_exceptions.UserPasswordNotFind()


def get_all(skip: int, limit: int, db: Session):
    return repository.get_all_users(skip, limit, db)


def get_user(user_id: int, db: Session):
    return repository.get_user(user_id, db)


def get_user_by_email(email: str, db: Session):
    return repository.get_user_by_email(email, db)


def update_user(user_id: int, update_user: User, db: Session):
    user = get_user(user_id, db)
    if user is None:
        raise UserNotFound()

    return repository.update_user(user, update_user, db)


def delete_user(user_id: int, db: Session):
    user = get_user(user_id, db)
    if user is None:
        raise UserNotFound()

    return repository.disable_user(user, db)


def restore_user(user_id: int, db: Session):
    user = get_user(user_id, db)
    if user is None:
        raise UserNotFound()

    return repository.enable_user(user, db)
