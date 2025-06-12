from pydantic import BaseModel, field_validator, ValidationError, model_validator
from api.exceptions import scheduling_exceptions

from datetime import date, datetime

class Scheduling(BaseModel):
    hour: int
    date: date
    name: str
    user_id: int
    phone: str

    @field_validator("hour")
    def validate_hour(cls, value):
        if (8 <= value <= 12) or (14 <= value <= 18):
            return value
        raise scheduling_exceptions.InvalidData("A hora deve estar 8 e 12 ou 14 e 18!")

    @field_validator("date")
    def validate_date(cls, value):
        if value >= date.today() :
            return value
        raise scheduling_exceptions.InvalidData("Não é possivel registrar para uma data anterior de hoje!")

    @model_validator(mode="before")
    def validate_hour_is_after_now(cls, value):
        dt = value["date"]

        date_object = datetime.strptime(dt, '%Y-%m-%d').date()


        if value["hour"] >= datetime.now().hour or date_object > date.today():
            return value
        raise scheduling_exceptions.InvalidData("Não é possivel registrar para um horario anterior que agora!")