from api.core.auth import Token
from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.services import auth_services as services
from api.core.database import get_db
from api.models.user import User
from api.models.dto.user_dto import (
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from api.exceptions.message import GenericError
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponseDTO,
    response_model_exclude_unset=True,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "Usuário foi Criado com Sucesso!",
        },
        400: {
            "model": GenericError,
            "description": "Usuário ou Email já existente com esses dados!",
        },
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
    status_code=201,
)
def sign_up(request: UserCreateDTO, db: Session = Depends(get_db)):
    return services.register_user(request, db)


@router.post(
    "/signin",
    response_model=Token,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "Login Realizado!",
        },
        400: {"model": GenericError, "description": "Email ou Senha Inválidos!"},
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado",
        },
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
    status_code=201,
)
def sign_in(request: UserLoginDTO, db: Session = Depends(get_db)):
    return services.login(request, db)


@router.get(
    "/getAllUsers",
    response_model=List[UserResponseDTO],
    response_model_exclude_unset=True,
    responses={
        201: {
            "model": List[UserResponseDTO],
            "description": "Lista de Usuários",
        },
        400: {
            "model": GenericError,
            "description": "Nenhum Usuário Cadastrado",
        },
        500: {"model": GenericError, "description": "Error no Servidor"},
    },
)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_all(skip, limit, db)


@router.get(
    "/getUser/{user_id}",
    response_model=UserResponseDTO,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": UserResponseDTO,
            "description": "Informações do Usuário",
        },
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado",
        },
        500: {"model": GenericError, "description": "Error no Servidor"},
    },
    status_code=200,
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return services.get_user(user_id, db)


@router.put(
    "/updateUser/{user_id}",
    response_model_exclude_unset=True,
    responses={
        204: {
            "description": "Dados Atualizados com Sucesso",
        },
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado",
        },
        500: {"model": GenericError, "description": "Error no Servidor"},
    },
    status_code=204,
)
def update_user(
    user_id: int, update_user_data: UserUpdateDTO, db: Session = Depends(get_db)
):
    return services.update_user(user_id, update_user_data, db)


@router.delete(
    "/deleteUser/{user_id}",
    response_model_exclude_unset=True,
    responses={
        204: {
            "description": "Usuário Deletado com sucesso!",
        },
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado!",
        },
        500: {"model": GenericError, "description": "Error no Servidor!"},
    },
    status_code=204,
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return services.delete_user(user_id, db)


@router.put(
    "/restoreUser/{user_id}",
    response_model=UserResponseDTO,
    response_model_exclude_unset=True,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "Usuário Restaurado",
        },
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado",
        },
        500: {"model": GenericError, "description": "Error no Servidor"},
    },
    status_code=201,
)
def restore_user(user_id: int, db: Session = Depends(get_db)):
    return services.restore_user(user_id, db)


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    return {"data": "OK"}
