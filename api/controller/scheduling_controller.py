from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.exceptions.message import GenericError
from api.models import scheduling
from api.models.enums.type import MsgReturn
from api.repository.scheduling_repository import SchedulingReposistory
from api.repository.user_repository import UserRepository
from api.services.scheduling_services import SchedulingService as services
from api.models.dto.scheduling_dto import Scheduling


router = APIRouter(prefix="/book", tags=["book"])


def get_scheduling_repo(db: Session = Depends(get_db)) -> SchedulingReposistory:
    return SchedulingReposistory(session=db)


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)


def get_scheduling_services(
    user_repo: UserRepository = Depends(get_user_repo),
    scheduling_repo: SchedulingReposistory = Depends(get_scheduling_repo),
) -> services:
    return services(scheduling_repo=scheduling_repo, user_repo=user_repo)


@router.post(
    "/",
    response_model=Scheduling,
    response_model_exclude_unset=True,
    status_code=201,
    responses={
        201: {
            "model": Scheduling,
            "description": "Book foi Criado com Sucesso!",
        },
        400: {
            "model": GenericError,
            "description": "Dados estão incorretos",
        },
        404: {
            "model": GenericError,
            "description": "Usuário com esse id não existe!",
        },
    },
)
def create_Scheduling(
    scheduling: Scheduling,
    scheduling_services: services = Depends(get_scheduling_services),
):
    return scheduling_services.create_scheduling(scheduling)


@router.get(
    "/",
    response_model=List[Scheduling],
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": List[Scheduling],
            "description": "Lista de Books",
        }
    },
)
def get_all_scheduling(
    skip: int = 0,
    limit: int = 10,
    scheduling_services: services = Depends(get_scheduling_services),
):
    return scheduling_services.get_all_schedulings(skip, limit)


@router.get(
    "/{scheduling_id}",
    response_model=Scheduling,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": Scheduling,
            "description": "Informações do Book",
        },
        404: {
            "model": GenericError,
            "description": "Book Não Encontrado",
        },
    },
)
def get_one_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.get_scheduling(scheduling_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/delete/{scheduling_id}",
    response_model=MsgReturn,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": MsgReturn,
            "description": "Book excluido",
        },
        404: {
            "model": GenericError,
            "description": "Book Não Encontrado",
        },
    },
)
def delete_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.delete_scheduling(scheduling_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/restore/{scheduling_id}",
    response_model=MsgReturn,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": MsgReturn,
            "description": "Book restaurado",
        },
        404: {
            "model": GenericError,
            "description": "Book Não Encontrado",
        },
    },
)
def restore_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.restore_scheduling(scheduling_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/update/{scheduling_id}",
    response_model=Scheduling,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": Scheduling,
            "description": "Book Atualizado",
        },
        404: {
            "model": GenericError,
            "description": "Book Não Encontrado",
        },
    },
)
def update_scheduling(
    scheduling_id: int, scheduling: Scheduling, db: Session = Depends(get_db)
):
    try:
        return scheduling_services.update_scheduling(scheduling_id, scheduling)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

