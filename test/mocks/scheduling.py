import datetime
from unittest.mock import MagicMock
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.repository.scheduling_repository import SchedulingReposistory
from api.repository.user_repository import UserRepository
from api.services.scheduling_services import SchedulingService

import pytest
from sqlalchemy.orm import Session

from test.mocks.user import (
    mock_user,
    mock_user_repository,
    mock_user_service,
    real_user_repository,
)


@pytest.fixture
def mock_scheduling_repository():
    return MagicMock(spec=SchedulingReposistory)


@pytest.fixture
def mock_scheduling_services(
    mock_scheduling_repository: SchedulingReposistory,
    mock_user_repository: UserRepository,
):
    return SchedulingService(
        scheduling_repo=mock_scheduling_repository, user_repo=mock_user_repository
    )


@pytest.fixture
def real_scheduling_repository(db_session_for_test: Session):
    """Fixture que fornece uma instância real do SchedulingRepository com uma sessão de teste."""
    return SchedulingReposistory(session=db_session_for_test)


@pytest.fixture
def real_scheduling_services(
    real_scheduling_repository: SchedulingReposistory,
    real_user_repository: UserRepository,
):
    """Fixture que fornece uma instância do SchedulingService com um repositório real (para testes de integração)."""
    return SchedulingService(
        scheduling_repo=real_scheduling_repository, user_repo=real_user_repository
    )


@pytest.fixture
def mock_scheduling(mock_user):
    return Scheduling(
        hour=12,
        date=datetime.datetime(2030, 6, 16),
        name="test",
        phone=1234567891234,
        user_id=1,
        user=mock_user,
        is_deleted=False,
    )


@pytest.fixture
def mock_scheduling_create():
    return scheduling_dto.Scheduling(
        hour=12,
        date=datetime.datetime(2030, 6, 16, 0, 0),
        name="test",
        phone="1234567891234",
        user_id=1,
    )


@pytest.fixture
def mock_scheduling_update():
    return scheduling_dto.Scheduling(
        hour=16,
        date=datetime.datetime(
            2040,
            5,
            10,
        ),
        name="test",
        phone="1234567891234",
        user_id=1,
    )


@pytest.fixture
def mock_scheduling_list(mock_user):
    return [
        Scheduling(
            hour=12,
            date=datetime.datetime(2030, 6, 16),
            name="test1",
            phone=1234567891231,
            user_id=1,
            user=mock_user,
            is_deleted=False,
        ),
        Scheduling(
            hour=8,
            date=datetime.datetime(2040, 4, 6),
            name="test2",
            phone=1234567891232,
            user_id=1,
            user=mock_user,
            is_deleted=False,
        ),
        Scheduling(
            hour=12,
            date=datetime.datetime(2037, 1, 17),
            name="test3",
            phone=1234567891233,
            user_id=1,
            user=mock_user,
            is_deleted=False,
        ),
        Scheduling(
            hour=14,
            date=datetime.datetime(2034, 7, 1),
            name="test4",
            phone=1234567891234,
            user_id=1,
            user=mock_user,
            is_deleted=False,
        ),
    ]
