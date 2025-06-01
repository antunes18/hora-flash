import datetime
from typing import Any

from sqlalchemy.orm import Session
from api.models.scheduling import Scheduling


def create(db: Session, scheduling: Scheduling) -> Scheduling:
    db.add(scheduling)
    db.commit()
    db.refresh(scheduling)
    return scheduling

def fing_scheduling_by_date_and_hour(db: Session, date: datetime.datetime, hour: int) -> Scheduling | None:
    return db.query(Scheduling).filter(Scheduling.date.startswith(date), Scheduling.hour == hour, Scheduling.is_deleted == False).first()

def find_all(db: Session) -> list:
    return db.query(Scheduling).all()

def find_one_scheduling(db: Session, id: int) -> Scheduling | None:
    return db.query(Scheduling).filter(Scheduling.id == id).first()

def delete_scheduling(db: Session, id: int) -> Scheduling | None:
    scheduling = find_one_scheduling(db, id)
    if scheduling:
        scheduling.is_deleted = True
        db.commit()
        db.refresh(scheduling)
        return scheduling
    else:
        return None

def restore_scheduling(db: Session, id: int) -> Scheduling | None:
    scheduling = find_one_scheduling(db, id)
    if scheduling:
        scheduling.is_deleted = False
        db.commit()
        db.refresh(scheduling)
        return scheduling
    else:
        return None

def update_scheduling(db: Session, id: int, scheduling: Scheduling) -> Scheduling | None:
    model = find_one_scheduling(db, id)
    if model:
        model.hour = scheduling.hour
        model.date = scheduling.date
        model.name = scheduling.name
        model.phone = scheduling.phone
        db.commit()
        db.refresh(model)
        return model
    else:
        return None
