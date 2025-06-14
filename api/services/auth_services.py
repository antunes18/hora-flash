from api.core import auth
from api.exceptions import user_exceptions
from api.models.dto.user_dto import UserCreateDTO, UserResponseDTO, UserLoginDTO

from api.repository.user_repository import UserRepository
from api.models.user import User
from api.core.auth import Token


class AuthServices:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def register_user(self, user: UserCreateDTO):
        if self.user_repo.get_user_by_email(user.email):
            raise user_exceptions.UserAlreadyExist()

        if self.user_repo.get_user_by_username(user.username):
            raise user_exceptions.UserInvalidUsername()

        if self.user_repo.get_user_by_phone_number(user.number):
            raise user_exceptions.UserPhoneNumberAlreadyUsed()

        user = User(
            username=user.username,
            email=user.email,
            number=user.number,
            password=auth.hash_password(user.password),
            disabled=False,
        )
        return self.user_repo.create_user(user)

    def login(self, user_login: UserLoginDTO) -> Token:
        user_data: UserResponseDTO = self.user_repo.get_user_by_email(user_login.email)

        if not user_data:
            raise user_exceptions.UserNotFound()

        if auth.verify_password(user_login.password, user_data.password):
            token = auth.sign(user_data)

            return Token(access_token=token)

        raise user_exceptions.UserPasswordNotFind()
