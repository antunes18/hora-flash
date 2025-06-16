from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session
from api.models.user import User
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserUpdateDTO
from api.models.enums.roles import Roles

from api.repository.user_repository import UserRepository
from api.services.auth_services import UserServices


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def mock_user_service(mock_user_repository: UserRepository):
    return UserServices(user_repo=mock_user_repository)


@pytest.fixture
def real_user_repository(db_session_for_test: Session):
    """Fixture que fornece uma instância real do UserRepository com uma sessão de teste."""
    return UserRepository(session=db_session_for_test)


@pytest.fixture
def real_users_services(user_repository: UserRepository):
    """Fixture que fornece uma instância do UserService com um repositório real (para testes de integração)."""
    return UserServices(user_repo=user_repository)


@pytest.fixture(scope="function")
def test_user_create():
    return UserCreateDTO(
        username="teste_de_user",
        email="teste111@teste.com",
        password="stringstri",
        number="1234567891234",
        confirm_password="stringstri",
        role=Roles.user,
    )


@pytest.fixture(scope="function")
def test_user_login():
    return UserLoginDTO(email="email@email.com", password="stringstri")


@pytest.fixture
def mock_user():
    return User(
        username="teste_de_user",
        email="teste@teste.com",
        password="stringstri",
        number="1234567891234",
        role="user",
        disabled=False,
    )


@pytest.fixture
def mock_user_create():
    return User(
        username="teste_de_user",
        email="teste@teste.com",
        number=1234567891234,
        password="stringstri",
        role="user",
        disabled=False,
    )


@pytest.fixture
def mock_user_update():
    return UserUpdateDTO(
        username="update_user",
        number="1234567891234",
        password="stringupdate",
        confirm_password="stringupdate",
    )


@pytest.fixture
def mock_list_user():
    return [
        User(
            username="teste_de_user1",
            email="teste1@teste.com",
            number="1234567891234",
            password="stringstri",
            role="user",
            disabled=False,
        ),
        User(
            username="teste_de_user2",
            email="teste2@teste.com",
            number="9876543210111",
            password="stringstri",
            role="user",
            disabled=False,
        ),
        User(
            username="teste_de_user3",
            email="teste3@teste.com",
            number="1234567891235",
            password="stringstri",
            role="user",
            disabled=False,
        ),
        User(
            username="teste_de_user4",
            email="teste4@teste.com",
            number="1234567891236",
            password="stringstri",
            role="user",
            disabled=False,
        ),
        User(
            username="teste_de_user5",
            email="teste5@teste.com",
            number="1234567891237",
            password="stringstri",
            role="user",
            disabled=False,
        ),
    ]
