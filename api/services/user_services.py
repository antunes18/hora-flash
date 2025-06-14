from fastapi import Query
from api.models.enums.roles import Roles
from api.exceptions import user_exceptions
from api.repository.user_repository import UserRepository
from api.models.user import User
from api.exceptions.user_exceptions import UserNotFound


class UserServices:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def get_all(self, skip: int, limit: int):
        return self.user_repo.get_all_users(skip, limit)

    def get_user(self, user_id: int):
        user = self.user_repo.get_user(user_id)
        if not user:
            raise user_exceptions.UserNotFound()

        return user

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise user_exceptions.UserNotFound()

        return user

    def update_user(self, user_id: int, update_user: User):
        user = self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        if self.user_repo.get_user_by_username(update_user.username):
            raise user_exceptions.UserInvalidUsername()

        if self.user_repo.get_user_by_phone_number(update_user.number):
            raise user_exceptions.UserPhoneNumberAlreadyUsed

        return self.user_repo.update_user(user, update_user)

    def delete_user(self, user_id: int):
        user = self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        return self.user_repo.disable_user(user)

    def restore_user(self, user_id: int):
        user = self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFound()

        return self.user_repo.enable_user(user)

    def change_role_user(self, user_id: int, role: Roles):
        user = self.user_repo.get_user(user_id=user_id)
        if user is None:
            raise UserNotFound()

        return self.user_repo.set_role(user, role=role)
