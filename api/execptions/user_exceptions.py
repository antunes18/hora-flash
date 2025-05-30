from fastapi import HTTPException


class UserInvalidData(HTTPException):
    def __init__(self, detail: str = "Dados Inválidos!"):
        super().__init__(status_code=422, detail=detail)


class UserNotFound(HTTPException):
    def __init__(self, detail: str = "Usuário Não Encontrado!"):
        super().__init__(status_code=404, detail=detail)


class UserAlereadyExist(HTTPException):
    def __init__(self, detail: str = "Usuário com esse Email já existe!"):
        super().__init__(status_code=404, detail=detail)
