from fastapi import responses
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO
from api.models.enums.roles import Roles
from api.services import auth_services as services
import pytest

from test.conftest import auth_headers, client
from test.mocks.user import mock_user_create, test_user_create, test_user_login


class TestUserServices:
    def test_register_user(self, test_user_create, db_session):
        response = services.register_user(test_user_create, db_session)
        assert mock_user_create.email == response.email
        assert mock_user_create.username == response.username
        assert mock_user_create.role == response.role
        assert mock_user_create.disabled == response.disabled
