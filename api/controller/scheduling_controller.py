from typing import List

from api.core.response_message import ResponseMessage
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.exceptions.message import GenericError
from api.exceptions import scheduling_exceptions  # Import scheduling_exceptions
from api.models.enums.type import MsgReturn
from api.repository.scheduling_repository import SchedulingReposistory
from api.repository.user_repository import UserRepository
from api.services.scheduling_services import SchedulingService as services
from api.models.dto.scheduling_dto import SchedulingDTO


router = APIRouter(prefix="/scheduling", tags=["scheduling"])


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
    response_model=SchedulingDTO,
    response_model_exclude_unset=True,
    status_code=201,
    responses={
        201: {
            "model": SchedulingDTO,
            "description": "Scheduling foi Criado com Sucesso!",
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
    scheduling: SchedulingDTO,
    scheduling_services: services = Depends(get_scheduling_services),
):
    return scheduling_services.create_scheduling(scheduling)


@router.get(
    "/",
    response_model=List[SchedulingDTO],
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": List[SchedulingDTO],
            "description": "Lista de Schedulings",
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
    "/user/{user_id}",
    response_model=List[SchedulingDTO],
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": List[SchedulingDTO],
            "description": "Lista de Schedulings do usuario",
        }
    },
)
def get_all_schedulings_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    scheduling_services: services = Depends(get_scheduling_services),
):
    print("aaaaaaaaaaaa")
    return scheduling_services.get_all_schedulings_by_user(skip, limit, user_id)


@router.get(
    "/{scheduling_id}",
    response_model=SchedulingDTO,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": SchedulingDTO,
            "description": "Informações do Scheduling",
        },
        404: {
            "model": GenericError,
            "description": "Scheduling Não Encontrado",
        },
    },
)
def get_one_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.get_scheduling(scheduling_id)
    except scheduling_exceptions.NotFound as e:  # Catch specific exception first
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/delete/{scheduling_id}",
    response_model=ResponseMessage,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": ResponseMessage,
            "description": "Scheduling excluído",
        },
        404: {
            "model": GenericError,
            "description": "Scheduling Não Encontrado",
        },
    },
)
def delete_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.delete_scheduling(scheduling_id)
    except scheduling_exceptions.NotFound as e:  # Catch specific exception first
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/restore/{scheduling_id}",
    response_model=ResponseMessage,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": ResponseMessage,
            "description": "Scheduling restaurado",
        },
        404: {
            "model": GenericError,
            "description": "Scheduling Não Encontrado",
        },
    },
)
def restore_scheduling(
    scheduling_id: int, scheduling_services: services = Depends(get_scheduling_services)
):
    try:
        return scheduling_services.restore_scheduling(scheduling_id)
    except scheduling_exceptions.NotFound as e:  # Catch specific exception first
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/update/{scheduling_id}",
    response_model=SchedulingDTO,
    response_model_exclude_unset=True,
    responses={
        200: {
            "model": SchedulingDTO,
            "description": "Scheduling Atualizado",
        },
        404: {
            "model": GenericError,
            "description": "Scheduling Não Encontrado",
        },
    },
)
def update_scheduling(
    scheduling_id: int,
    scheduling: SchedulingDTO,
    scheduling_services: services = Depends(get_scheduling_services),
):
    try:
        return scheduling_services.update_scheduling(scheduling_id, scheduling)
    except scheduling_exceptions.NotFound as e:  # Catch specific exception first
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
