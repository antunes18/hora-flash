from api.core.auth import Token
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.repository.user_repository import UserRepository
from api.services.auth_services import AuthServices as services
from api.core.database import get_db
from api.models.dto.user_dto import (
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
)
from api.exceptions.message import GenericError

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
            "description": "Usuário Já Existente com esses dados!",
        },
        401: {
            "model": GenericError,
            "description": "Usuário com esse Email já Existe!",
        },
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
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
        403: {"model": GenericError, "description": "Email ou Senha Inválidos!"},
        404: {
            "model": GenericError,
            "description": "Usuário Não Encontrado",
        },
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
)
def sign_in(
    request: UserLoginDTO, user_services: services = Depends(get_user_services)
):
    return user_services.login(request)
