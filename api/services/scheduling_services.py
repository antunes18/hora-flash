from datetime import date, datetime

from sqlalchemy.orm import Session

from api.exceptions import scheduling_exceptions, user_exceptions
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.repository.scheduling_repository import SchedulingReposistory
from api.repository.user_repository import UserRepository


class SchedulingService:
    def __init__(
        self, scheduling_repo: SchedulingReposistory, user_repo: UserRepository
    ):
        self.scheduling_repo = scheduling_repo
        self.user_repo = user_repo

    def create_scheduling(self, dto: scheduling_dto):


        if (dto.hour < 8) or ( 14 > dto.hour > 12) or (dto.hour > 18):
            raise scheduling_exceptions.InvalidData("A hora deve estar 8 e 12 ou 14 e 18!")

        if dto.date < date.today() :
            raise scheduling_exceptions.InvalidData("Não é possivel registrar para uma data anterior de hoje!")

        try:
            appointment_datetime = datetime.combine(dto.date, datetime.min.time()).replace(hour=dto.hour)
        except TypeError:
            raise scheduling_exceptions.InvalidData("Data ou hora inválida para o agendamento.")

        if appointment_datetime < datetime.now():
            raise scheduling_exceptions.InvalidData(
                "Não é possível registrar um agendamento para uma data ou hora no passado.")

        existing = self.scheduling_repo.find_scheduling_by_date_and_hour_and_user(
            dto.date, dto.hour, dto.user_id
        )
        user = self.user_repo.get_user(dto.user_id)

        if existing:
            raise scheduling_exceptions.AlreadyExist()

        if not user:
            raise user_exceptions.UserNotFound()

        scheduling = Scheduling(
            hour=dto.hour,
            date=dto.date,
            name=dto.name,
            user_id=dto.user_id,
            phone=dto.phone,
        )
        return self.scheduling_repo.create(scheduling=scheduling)

    def get_all_schedulings(self, skip: int, limit: int):
        return self.scheduling_repo.find_all(skip, limit)

    def get_all_schedulings_by_user(self, skip: int, limit: int, user_id: int):
        return self.scheduling_repo.find_all_by_user(skip, limit, user_id)

    def get_scheduling(self, scheduling_id: int):
        scheduling = self.scheduling_repo.find_one_scheduling(scheduling_id)

        if scheduling:
            return scheduling
        else:
            raise scheduling_exceptions.NotFound()

    def delete_scheduling(self, scheduling_id: int):
        scheduling = self.scheduling_repo.delete_scheduling(scheduling_id)

        if scheduling:
            return {"message": "book deleted"}
        else:
            raise scheduling_exceptions.NotFound()

    def restore_scheduling(self, scheduling_id: int):
        scheduling = self.scheduling_repo.restore_scheduling(scheduling_id)

        if scheduling:
            return {"message": "book restored"}
        else:
            raise scheduling_exceptions.NotFound()

    def update_scheduling(self, scheduling_id: int, scheduling_dto: scheduling_dto.Scheduling): # Parameter renamed
        existing_scheduling = self.scheduling_repo.find_one_scheduling(scheduling_id)

        if not existing_scheduling:
            raise scheduling_exceptions.NotFound()

        # Update fields from DTO
        existing_scheduling.hour = scheduling_dto.hour
        existing_scheduling.date = scheduling_dto.date
        existing_scheduling.name = scheduling_dto.name
        existing_scheduling.phone = scheduling_dto.phone
        # user_id is not updated as per instruction

        # Call repository to save changes
        return self.scheduling_repo.update_scheduling(scheduling_id, existing_scheduling)
