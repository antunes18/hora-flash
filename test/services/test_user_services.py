from logging import disable
from unittest.mock import Mock
from fastapi import responses
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO
from api.services.auth_services import UserServices
from api.models.user import User

from test.mocks.user import (
    UserResponseDTO,
    mock_user,
    mock_list_user,
    mock_user_repository,
    mock_user_service,
    mock_user_update,
    test_user_create,
)


class TestUserServices:
    def test_register_user(
        self,
        test_user_create: UserCreateDTO,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
        mock_user: User,
    ):
        mock_user_repository.get_user_by_email.return_value = None
        mock_user_repository.create_user.return_value = mock_user
        response = mock_user_service.register_user(test_user_create)

        assert response is not None
        assert response.email == test_user_create.email
        assert response.username == test_user_create.username
        assert response.number == test_user_create.number
        assert response.role == test_user_create.role
        assert response.disabled == False

    def test_get_all(
        self,
        mock_list_user: list[User],
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_all_users.return_value = mock_list_user
        response = mock_user_service.get_all(skip=0, limit=100)
        assert response is not None
        assert len(response) == len(mock_list_user)
        assert response == mock_list_user

    def test_get_user(
        self,
        mock_user: User,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_user.return_value = mock_user

        response = mock_user_service.get_user(user_id=1)

        assert response is not None

        assert response.email == mock_user.email
        assert response.username == mock_user.username
        assert response.role == mock_user.role
        assert response.disabled == mock_user.disabled

    def test_get_user_by_email(
        self,
        mock_user: User,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_user_by_email.return_value = mock_user

        response = mock_user_service.get_user_by_email("teste@teste.com")

        assert response is not None

        assert response.email == mock_user.email
        assert response.username == mock_user.username
        assert response.role == mock_user.role
        assert response.disabled == mock_user.disabled

    def test_update_user(
        self,
        mock_user: User,
        mock_user_update: User,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_user.return_value = mock_user
        mock_user_repository.update_user.return_value = mock_user_update

        response = mock_user_service.update_user(1, mock_user_update)

        assert response is not None
        assert response == mock_user_update

    def test_delete_user(
        self,
        mock_user: User,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_user.return_value = mock_user

        disabled_user = mock_user
        disabled_user.disabled = True

        mock_user_repository.disable_user.return_value = disabled_user
        response = mock_user_service.delete_user(1)

        assert response is not None
        assert response.disabled is True

    def test_restore_user(
        self,
        mock_user: User,
        mock_user_service: UserServices,
        mock_user_repository: Mock,
    ):
        mock_user_repository.get_user.return_value = mock_user

        restored_user = mock_user
        restored_user.disabled = False

        mock_user_repository.enable_user.return_value = restored_user

        response = mock_user_service.restore_user(1)

        assert response is not None
        assert response.disabled is False
