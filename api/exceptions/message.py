from fastapi import status
from pydantic import BaseModel


class GenericError(BaseModel):
    status_code: int
    message: str
