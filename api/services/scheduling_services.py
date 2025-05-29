from sqlalchemy.orm import Session
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.repository import scheduling_repository as repository


def create_scheduling(dto: scheduling_dto, db: Session):
    scheduling = Scheduling(
        hour=dto.hour,
        date=dto.date,
        name=dto.name
    )
    return repository.create(db=db, scheduling=scheduling)
