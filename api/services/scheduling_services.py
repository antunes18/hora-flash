from sqlalchemy.orm import Session

from api.exceptions import scheduling_exceptions, user_exceptions
from api.models.dto import scheduling_dto
from api.models.scheduling import Scheduling
from api.repository import scheduling_repository as repository
from api.repository import user_repository as user_repository


def create_scheduling(dto: scheduling_dto, db: Session):
    existing = repository.fing_scheduling_by_date_and_hour(db, dto.date, dto.hour)
    user = user_repository.get_user(dto.user_id, db)

    if existing:
         raise scheduling_exceptions.AlreadyExist()

    if not user:
        raise user_exceptions.UserNotFound()

    print(existing)
    scheduling = Scheduling(
        hour=dto.hour,
        date=dto.date,
        name=dto.name,
        user_id=dto.user_id,
        phone=dto.phone,
    )
    return repository.create(db=db, scheduling=scheduling)


def get_all_schedulings(skip: int, limit: int, db: Session):
    return repository.find_all(skip, limit, db)


def get_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.find_one_scheduling(db, scheduling_id)

    if scheduling:
        return scheduling
    else:
        raise scheduling_exceptions.NotFound()


def delete_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.delete_scheduling(db, scheduling_id)

    if scheduling:
        return {"message": "book deleted"}
    else:
        raise scheduling_exceptions.NotFound()


def restore_scheduling(db: Session, scheduling_id: int):
    scheduling = repository.restore_scheduling(db, scheduling_id)

    if scheduling:
        return {"message": "book restored"}
    else:
        raise scheduling_exceptions.NotFound()



def update_scheduling(db: Session, scheduling_id: int, scheduling: Scheduling):
    scheduling = repository.update_scheduling(db, scheduling_id, scheduling)
    if scheduling:
        return repository.update_scheduling(db, scheduling_id, scheduling)
    else:
        raise scheduling_exceptions.NotFound()

