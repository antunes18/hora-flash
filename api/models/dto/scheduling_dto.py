from pydantic import BaseModel, field_validator, ValidationError, model_validator
from api.exceptions import scheduling_exceptions

from datetime import date, datetime

class Scheduling(BaseModel):
    date: date
    hour: int
    name: str
    user_id: int
    phone: str


