from pydantic import BaseModel, field_validator, ValidationError
from datetime import date

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
        raise ValidationError("hour must be between 8 and 12 ")

    @field_validator("date")
    def validate_date(cls, value):
        if value >= date.today():
            return value
        raise ValidationError("date must be after today")
