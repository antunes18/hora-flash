from operator import le
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.models.user import User
from api.repository.scheduling_repository import SchedulingReposistory
from test.mocks.scheduling import (
    mock_scheduling_list,
    real_scheduling_repository,
    mock_scheduling,
    mock_scheduling_update,
)
from test.mocks.user import mock_user


class TestScheulingRepository:
    def test_create(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_user: User,
    ):
        data = real_scheduling_repository.create(mock_scheduling)

        assert data is not None
        assert data.id == mock_scheduling.id
        assert data.date == mock_scheduling.date
        assert data.hour == mock_scheduling.hour
        assert data.name == mock_scheduling.name
        assert data.phone == mock_scheduling.phone
        assert data.user_id == mock_scheduling.user_id
        assert data.user == mock_scheduling.user
        assert data.is_deleted == mock_scheduling.is_deleted

    def test_find_scheduling_by_date_and_hour(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_user: User,
    ):
        real_scheduling_repository.session.add(mock_scheduling)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.find_scheduling_by_date_and_hour(
            date=mock_scheduling.date, hour=mock_scheduling.hour
        )
        assert data is not None
        assert data.id == mock_scheduling.id
        assert data.date == mock_scheduling.date
        assert data.hour == mock_scheduling.hour
        assert data.name == mock_scheduling.name
        assert data.phone == mock_scheduling.phone
        assert data.user_id == mock_scheduling.user_id
        assert data.user == mock_scheduling.user
        assert data.is_deleted == mock_scheduling.is_deleted

    def test_find_all(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_scheduling_list: list[Scheduling],
        mock_user: User,
    ):
        real_scheduling_repository.session.add_all(mock_scheduling_list)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.find_all(skip=0, limit=10)

        assert data is not None
        assert len(data) == len(mock_scheduling_list)

    def test_find_one_scheduling(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_user: User,
    ):
        real_scheduling_repository.session.add(mock_scheduling)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.find_one_scheduling(mock_scheduling.id)

        assert data is not None
        assert data.id == mock_scheduling.id
        assert data.date == mock_scheduling.date
        assert data.hour == mock_scheduling.hour
        assert data.name == mock_scheduling.name
        assert data.phone == mock_scheduling.phone
        assert data.user_id == mock_scheduling.user_id
        assert data.user == mock_scheduling.user
        assert data.is_deleted == mock_scheduling.is_deleted

    def test_delete_scheduling(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_user: User,
    ):
        real_scheduling_repository.session.add(mock_scheduling)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.delete_scheduling(mock_scheduling.id)

        assert data is not None
        assert data.id == mock_scheduling.id
        assert data.date == mock_scheduling.date
        assert data.hour == mock_scheduling.hour
        assert data.name == mock_scheduling.name
        assert data.phone == mock_scheduling.phone
        assert data.user_id == mock_scheduling.user_id
        assert data.user == mock_scheduling.user
        assert data.is_deleted == mock_scheduling.is_deleted

    def test_restore_scheduling(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_user: User,
    ):
        real_scheduling_repository.session.add(mock_scheduling)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.restore_scheduling(mock_scheduling.id)

        assert data is not None
        assert data.id == mock_scheduling.id
        assert data.date == mock_scheduling.date
        assert data.hour == mock_scheduling.hour
        assert data.name == mock_scheduling.name
        assert data.phone == mock_scheduling.phone
        assert data.user_id == mock_scheduling.user_id
        assert data.user == mock_scheduling.user
        assert data.is_deleted == mock_scheduling.is_deleted

    def test_update_scheduling(
        self,
        real_scheduling_repository: SchedulingReposistory,
        mock_scheduling: Scheduling,
        mock_scheduling_update: scheduling_dto.Scheduling,
        mock_user: User,
    ):
        real_scheduling_repository.session.add(mock_scheduling)
        real_scheduling_repository.session.commit()

        data = real_scheduling_repository.update_scheduling(
            mock_scheduling.id, mock_scheduling_update
        )

        assert data is not None
        assert data.date == mock_scheduling_update.date
        assert data.hour == mock_scheduling_update.hour
        assert data.name == mock_scheduling_update.name
        assert data.phone == mock_scheduling_update.phone
        assert data.user_id == mock_scheduling_update.user_id
