from sqlalchemy.orm import Session
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.repository import scheduling_repository as repository


def create_scheduling(dto: scheduling_dto, db: Session):

    existing = repository.fing_scheduling_by_date_and_hour(db, dto.date, dto.hour)

    if existing:
         return {"message": "book already exists"}

    print(existing)
    scheduling = Scheduling(
        hour=dto.hour,
        date=dto.date,
        name=dto.name,
        phone=dto.phone,
    )
    return repository.create(db=db, scheduling=scheduling)
