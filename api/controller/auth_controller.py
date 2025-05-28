from api.core.jwt_bearer import JwtBearer
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.services import auth_services as services
from api.core import auth
from api.core.database import get_db
from api.models.dto.user_dto import UserCreateDTO, UserLoginDTO, UserResponseDTO


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponseDTO,
)
def sign_up(request: UserCreateDTO, db: Session = Depends(get_db)):
    try:
        return services.register_user(request, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.post(
    "/signin",
    response_model=UserResponseDTO,
    responses={},
)
def sign_in(request: UserLoginDTO, db: Session = Depends(get_db)):
    try:
        return services.login(request, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teste", dependencies=[Depends(JwtBearer())])
def teste():
    try:
        return {"data": "OK"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ERROR: {e}"
        )
