from unittest.mock import AsyncMock
import pytest
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO
from api.services.auth_services import UserServices

from test.mocks.user import (
    mock_user_create,
    mock_user_repository,
    mock_user_service,
    test_user_create,
)


class TestUserServices:
    @pytest.mark.asyncio
    async def test_register_user(
        self,
        test_user_create,
        mock_user_service: UserServices,
        mock_user_repository: AsyncMock,
    ):
        mock_user_repository.get_user_by_email.return_value = None
        response = await mock_user_service.register_user(test_user_create)

        assert mock_user_create.email == response.email
        assert mock_user_create.username == response.username
        assert mock_user_create.role == response.role
        assert mock_user_create.disabled == response.disabled

    # def test_get_all(self, db_session):
    #     response = services.get_all(skip=0, limit=100, db=db_session)

    #       assert response is not None

    # def test_get_user(self, db_session):
    #    db_session.add(mock_user_create)
    #    db_session.commit()
    #    response = services.get_user(user_id=1, db=db_session)

    #    assert response is not None

    #   assert response.email == mock_user_create.email
    #  assert response.username == mock_user_create.username
    # assert response.role == mock_user_create.role
    # assert response.disabled == mock_user_create.disabled

    # def test_get_user_by_email(self, db_session):
    #   response = services.get_user_by_email(
    #        email=mock_user_create.email, db=db_session
    #    )

    #        assert response is not None

    def test_update_user(self):
        pass

    def test_delete_user(self):
        pass

    def test_restore_user(self):
        pass
