from pydantic import BaseModel
from datetime import date

from sqlalchemy import between


class Scheduling(BaseModel):
    hour: int
    date: date
    name: str

