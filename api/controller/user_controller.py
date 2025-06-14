from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.repository.user_repository import UserRepository
from api.services.user_services import UserServices as services
from api.core.database import get_db
from api.models.dto.user_dto import (
    UserResponseDTO,
    UserUpdateDTO,
)
from api.models.enums.roles import Roles
from api.exceptions.message import GenericError
from typing import List

router = APIRouter(prefix="/user", tags=["Users"])


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)


def get_user_services(
    user_repo: UserRepository = Depends(get_user_repo),
) -> services:
    return services(user_repo=user_repo)


@router.get(
    "/",
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
    "/{user_id}",
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
    "/{user_id}",
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
    "/{user_id}",
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
    "/restore/{user_id}",
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
    status_code=204,
    dependencies=[Depends(JwtBearer())],
)
def restore_user(user_id: int, user_services: services = Depends(get_user_services)):
    return user_services.restore_user(user_id)


@router.put(
    "/setRole/{user_id}",
    response_model_exclude_unset=True,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "Role Alterada com sucesso",
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
def set_role_user(
    user_id: int, role: Roles, user_services: services = Depends(get_user_services)
):
    return user_services.change_role_user(user_id, role)
