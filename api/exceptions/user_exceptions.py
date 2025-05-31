from fastapi import HTTPException
from pydantic import BaseModel


class GernericError(BaseModel):
    message: str
    status_code: int


class UserInvalidData(HTTPException):
    def __init__(self, detail: str = "Dados Inválidos!"):
        super().__init__(status_code=422, detail=detail)


class UserNotFound(HTTPException):
    def __init__(self, detail: str = "Usuário Não Encontrado!"):
        super().__init__(status_code=404, detail=detail)


class UserAlreadyExist(HTTPException):
    def __init__(self, detail: str = "Usuário com esse Email já existe!"):
        super().__init__(status_code=404, detail=detail)


class UserPasswordNotFind(HTTPException):
    def __init__(self, detail: str = "Senha incorreta!"):
        super().__init__(status_code=403, detail=detail)
