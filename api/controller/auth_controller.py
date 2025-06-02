from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.services import auth_services as services
from api.core.database import get_db
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO
from api.execptions.message import GenericError


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
            "description": "Usuário Já Existente com esses dados!",
        },
        401: {
            "model": GenericError,
            "description": "Usuário com esse Email já Existe!",
        },
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
)
def sign_up(request: UserCreateDTO, db: Session = Depends(get_db)):
    return services.register_user(request, db)


@router.post(
    "/signin",
    response_model=UserResponseDTO,
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
def sign_in(request: UserLoginDTO, db: Session = Depends(get_db)):
    return services.login(request, db)


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    return {"data": "OK"}
