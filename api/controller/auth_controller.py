from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.services import auth_services as services
from api.core.database import get_db
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO
from api.exceptions.message import GenericError
from api.exceptions import user_exceptions


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
        422: {"model": GenericError, "description": "Dados Invalidos!"},
    },
)
def sign_up(request: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        return services.register_user(request, db)

    except user_exceptions.UserAlreadyExist:
        raise user_exceptions.UserAlreadyExist(email=request.email)


@router.post(
    "/signin",
    response_model=UserLoginDTO,
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
    try:
        return services.login(request, db)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    try:
        return {"data": "OK"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR: {e}"
        )
