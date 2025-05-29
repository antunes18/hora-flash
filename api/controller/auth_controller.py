from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends, HTTPException, responses, status
from sqlalchemy.orm import Session
from api.services import auth_services as services
from api.core import auth
from api.core.database import get_db
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO
from api.execptions.message import Message

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
        400: {"model": Message, "description": "Usuário Já Existente com esses dados!"},
        422: {"model": Message, "description": "Dados Invalidos!"},
    },
)
def sign_up(request: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        return services.register_user(request, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/signin",
    response_model=UserResponseDTO,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "Login Realizado!",
        },
        403: {"model": Message, "description": "Email ou Senha Inválidos!"},
        422: {"model": Message, "description": "Dados Invalidos!"},
    },
)
def sign_in(request: UserLoginDTO, db: Session = Depends(get_db)):
    try:
        return services.login(request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    return {"result": "Yes"}
