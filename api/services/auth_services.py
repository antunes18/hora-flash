from api.core import auth
from sqlalchemy.orm import Session
from api.exceptions import user_exceptions
from api.models.dto.user_dto import UserCreateDTO, UserResponseDTO, UserLoginDTO

from api.repository.user_repository import UserRepository
from api.models.user import User
from api.core.auth import Token
from api.exceptions.user_exceptions import UserNotFound


class UserServices:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def register_user(self, user: UserCreateDTO):
        existing = await self.user_repo.get_user_by_email(user.email)
        if existing:
            raise user_exceptions.UserAlreadyExist()

        user = User(
            username=user.username,
            email=user.email,
            password=auth.hash_password(user.password),
            role=user.role,
            disabled=False,
        )
        return await self.user_repo.create_user(user)

    def login(self, user_login: UserLoginDTO) -> Token:
        user_data: UserResponseDTO = self.user_repo.get_user_by_email(user_login.email)
        if not user_data:
            raise user_exceptions.UserNotFound()

        if auth.verify_password(user_login.password, user_data.password):
            token = auth.sign(user_data)

            return Token(access_token=token)

        raise user_exceptions.UserPasswordNotFind()

    async def get_all(self, skip: int, limit: int):
        return await self.user_repo.get_all_users(skip, limit)

    async def get_user(self, user_id: int):
        return await self.user_repo.get_user(user_id)

    async def get_user_by_email(self, email: str):
        return await self.user_repo.get_user_by_email(email)

    async def update_user(self, user_id: int, update_user: User):
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        return await self.user_repo.update_user(user, update_user)

    async def delete_user(self, user_id: int):
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        return await self.user_repo.disable_user(user)

    async def restore_user(self, user_id: int):
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        return await self.user_repo.enable_user(user)
