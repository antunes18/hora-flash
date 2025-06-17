import re
from unittest.mock import Mock

from fastapi import responses
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.models.user import User
from api.repository.scheduling_repository import SchedulingReposistory
from api.services.scheduling_services import SchedulingService
from test.mocks.scheduling import (
    mock_scheduling_create,
    mock_scheduling_services,
    mock_scheduling_repository,
    mock_scheduling,
    mock_scheduling_create,
    mock_scheduling_list,
    mock_scheduling_update,
)
from test.mocks.user import mock_user_repository, mock_user


class TestScheulingServices:
    def test_create_scheduling(
        self,
        mock_scheduling_services: SchedulingService,
        mock_scheduling_repository: Mock,
        mock_user_repository: Mock,
        mock_scheduling: Scheduling,
        mock_scheduling_create: scheduling_dto.Scheduling,
    ):
        mock_scheduling_repository.find_scheduling_by_date_and_hour.return_value = None
        mock_user_repository.get_user.return_value = mock_user
        mock_scheduling_repository.create.return_value = mock_scheduling

        response = mock_scheduling_services.create_scheduling(mock_scheduling_create)

        assert response is not None
        assert response.hour == mock_scheduling.hour
        assert response.date == mock_scheduling.date
        assert response.name == mock_scheduling.name
        assert response.phone == mock_scheduling.phone
        assert response.user_id == mock_scheduling.user_id

    def test_get_all_sheduling(
        self,
        mock_scheduling_repository: Mock,
        mock_scheduling_services: SchedulingService,
        mock_user: User,
    ):
        mock_scheduling_repository.find_all.return_value = mock_scheduling_list

        response = mock_scheduling_services.get_all_schedulings(skip=0, limit=10)

        assert response is not None

    def test_get_scheduling(
        self,
        mock_scheduling_repository: Mock,
        mock_scheduling_services: SchedulingService,
        mock_scheduling: Scheduling,
    ):
        mock_scheduling_repository.find_one_scheduling.return_value = mock_scheduling

        response = mock_scheduling_services.get_scheduling(mock_scheduling.id)

        assert response is not None

        assert response.hour == mock_scheduling.hour
        assert response.date == mock_scheduling.date
        assert response.name == mock_scheduling.name
        assert response.phone == mock_scheduling.phone
        assert response.user_id == mock_scheduling.user_id

    def test_delete_scheduling(
        self,
        mock_scheduling_repository: Mock,
        mock_scheduling_services: SchedulingService,
        mock_scheduling: Scheduling,
    ):
        mock_scheduling_repository.delete_scheduling(
            mock_scheduling.id
        ).return_value = mock_scheduling
        response = mock_scheduling_services.delete_scheduling(mock_scheduling.id)
        assert response is not None

    def test_restore_scheduling(
        self,
        mock_scheduling_repository: Mock,
        mock_scheduling_services: SchedulingService,
        mock_scheduling: Scheduling,
    ):
        mock_scheduling_repository.restore_scheduling(
            mock_scheduling.id
        ).return_value = mock_scheduling

        response = mock_scheduling_services.restore_scheduling(mock_scheduling.id)
        assert response is not None

    def test_update_scheduling(
        self,
        mock_scheduling_repository: Mock,
        mock_scheduling_services: SchedulingService,
        mock_scheduling: Scheduling,
        mock_scheduling_update: scheduling_dto.Scheduling,
    ):
        mock_scheduling_repository.find_one_scheduling.return_value = mock_scheduling
        mock_scheduling_repository.update_scheduling.return_value = (
            mock_scheduling_update
        )

        response = mock_scheduling_services.update_scheduling(
            mock_scheduling.id, mock_scheduling_update
        )

        assert response is not None
        assert response.hour == mock_scheduling_update.hour
        assert response.date == mock_scheduling_update.date
        assert response.name == mock_scheduling_update.name
        assert response.phone == mock_scheduling_update.phone
        assert response.user_id == mock_scheduling_update.user_id
