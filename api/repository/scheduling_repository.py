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
    return db.query(Scheduling).filter(Scheduling.date.startswith(date), Scheduling.hour == hour).first()

#
# def find_all(db: Session) -> list:
#     return db.query(User).all()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()
