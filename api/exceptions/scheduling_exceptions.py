from fastapi import HTTPException
from pydantic import BaseModel


class GernericError(BaseModel):
    message: str
    status_code: int


class InvalidData(HTTPException):
    def __init__(self, detail: str = "Dados Inválidos!"):
        super().__init__(status_code=400, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: str = "Reserva Não Encontrado!"):
        super().__init__(status_code=404, detail=detail)


class AlreadyExist(HTTPException):
    def __init__(self, detail: str = "Horario nesse dia não disponivel!"):
        super ().__init__(status_code=400, detail=detail)



