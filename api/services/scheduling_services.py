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


def get_all_schedulings(db: Session):
    return repository.find_all(db=db)

def get_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.find_one_scheduling(db, scheduling_id)

    if scheduling:
        return scheduling
    else:
        return {"message": "book does not exists"}

def delete_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.delete_scheduling(db, scheduling_id)

    if scheduling:
        return {"message": "book deleted"}
    else:
        return {"message": "book does not exists"}

def restore_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.restore_scheduling(db, scheduling_id)

    if scheduling:
        return {"message": "book restored"}
    else:
        return {"message": "book does not exists"}

def update_scheduling(db: Session, scheduling_id: int, scheduling: Scheduling):
    scheduling = repository.update_scheduling(db, scheduling_id, scheduling)
    if scheduling:
        return repository.update_scheduling(db, scheduling_id, scheduling)
    else:
        return {"message": "book does not exists"}