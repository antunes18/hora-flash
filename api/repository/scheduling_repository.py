import datetime

from sqlalchemy.orm import Session

from api.models.scheduling import Scheduling


class SchedulingReposistory:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, scheduling: Scheduling) -> Scheduling:
        self.session.add(scheduling)
        self.session.commit()
        self.session.refresh(scheduling)
        return scheduling

    def fing_scheduling_by_date_and_hour(
        self, date: datetime.datetime, hour: int
    ) -> Scheduling | None:
        return (
            self.session.query(Scheduling)
            .filter(
                Scheduling.date.startswith(date),
                Scheduling.hour == hour,
                Scheduling.is_deleted == False,
            )
            .first()
        )

    def find_all(self, skip: int, limit: int) -> list:
        return (
            self.session.query(Scheduling)
            .filter(Scheduling.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def find_one_scheduling(self, id: int) -> Scheduling | None:
        return self.session.query(Scheduling).filter(Scheduling.id == id).first()

    def delete_scheduling(self, id: int) -> Scheduling | None:
        scheduling = self.find_one_scheduling(id)
        if scheduling:
            scheduling.is_deleted = True
            self.session.commit()
            self.session.refresh(scheduling)
            return scheduling
        else:
            return None

    def restore_scheduling(self, id: int) -> Scheduling | None:
        scheduling = self.find_one_scheduling(id)
        if scheduling:
            scheduling.is_deleted = False
            self.session.commit()
            self.session.refresh(scheduling)
            return scheduling
        else:
            return None

    def update_scheduling(self, id: int, scheduling: Scheduling) -> Scheduling | None:
        model = self.find_one_scheduling(id)
        if model:
            model.hour = scheduling.hour
            model.date = scheduling.date
            model.name = scheduling.name
            model.phone = scheduling.phone
            self.session.commit()
            self.session.refresh(model)
            return model
        else:
            return None
