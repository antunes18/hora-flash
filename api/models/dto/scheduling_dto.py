from pydantic import BaseModel, field_validator, ValidationError, model_validator
from api.exceptions import scheduling_exceptions

from datetime import date, datetime


class Scheduling(BaseModel):
    date: date
    hour: int
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
        if value >= date.today():
            return value
        raise scheduling_exceptions.InvalidData(
            "Não é possivel registrar para uma data anterior de hoje!"
        )

    @field_validator("hour")
    def validate_datetime_is_in_the_future(cls, value, info):
        # Access data from the model instance through info.data
        appointment_date = info.data.get("date")

        # Ensure that 'date' is present in the data, otherwise skip validation or handle error
        if not appointment_date:
            # This case should ideally be caught by Pydantic's own validation if 'date' is a required field.
            # If 'date' can be optional, this validation might need adjustment.
            raise scheduling_exceptions.InvalidData(
                "A data do agendamento é necessária."
            )

        try:
            # Combine date and hour to create a datetime object
            # Assuming 'value' is the hour. Ensure it's an integer.
            appointment_datetime = datetime.combine(
                appointment_date, datetime.min.time()
            ).replace(hour=value)
        except TypeError:
            # Handle cases where appointment_date is not a date object or value is not a valid hour
            raise scheduling_exceptions.InvalidData(
                "Data ou hora inválida para o agendamento."
            )

        if appointment_datetime >= datetime.now():
            return value

        raise scheduling_exceptions.InvalidData(
            "Não é possível registrar um agendamento para uma data ou hora no passado."
        )
