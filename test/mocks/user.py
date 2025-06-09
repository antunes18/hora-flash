import pytest
from api.models.user import User
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO
from api.models.enums.roles import Roles
from unittest.mock import AsyncMock

from api.repository.user_repository import UserRepository


@pytest.fixture
def mock_user_UserRepository():
    mock_repo = AsyncMock(spec=UserRepository)
    return mock_repo


@pytest.fixture
def mock_user_service(mock_user_UserRepository: AsyncMock):
    return UserService(user_repo=mock_user_UserRepository)


@pytest.fixture(scope="function")
def test_user_create():
    return UserCreateDTO(
        username="Teste",
        email="email@email.com",
        password="stringstri",
        confirm_password="stringstri",
        role=Roles.user,
    )


@pytest.fixture(scope="function")
def test_user_login():
    return UserLoginDTO(email="email@email.com", password="stringstri")


mock_user_create = User(
    username="Teste",
    email="email@email.com",
    password="stringstri",
    role="user",
    disabled=False,
)
