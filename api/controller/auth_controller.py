from api.core.auth import Token
from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.repository.user_repository import UserRepository
from api.services.auth_services import UserServices as services
from api.core.database import get_db
from api.models.dto.user_dto import (
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from api.exceptions.message import GenericError
from typing import List

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)


def get_user_services(
    user_repo: UserRepository = Depends(get_user_repo),
) -> services:
    return services(user_repo=user_repo)


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
def sign_up(
    request: UserCreateDTO, user_services: services = Depends(get_user_services)
):
    return user_services.register_user(request)


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
def sign_in(
    request: UserLoginDTO, user_services: services = Depends(get_user_services)
):
    return user_services.login(request)


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
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    user_services: services = Depends(get_user_services),
):
    return user_services.get_all(skip, limit)


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
def get_user(user_id: int, user_services: services = Depends(get_user_services)):
    return user_services.get_user(user_id)


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
    dependencies=[Depends(JwtBearer())],
)
def update_user(
    user_id: int,
    update_user_data: UserUpdateDTO,
    user_services: services = Depends(get_user_services),
):
    return user_services.update_user(user_id, update_user_data)


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
    dependencies=[Depends(JwtBearer())],
)
def delete_user(user_id: int, user_services: services = Depends(get_user_services)):
    return user_services.delete_user(user_id)


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
    dependencies=[Depends(JwtBearer())],
)
def restore_user(user_id: int, user_services: services = Depends(get_user_services)):
    return user_services.restore_user(user_id)


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    return {"data": "OK"}
