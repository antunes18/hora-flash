from fastapi import status
from pydantic import BaseModel


class GernericError(BaseModel):
    status_code: int
    message: str
