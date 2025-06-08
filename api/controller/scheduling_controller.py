from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.exceptions.message import GenericError
from api.models.enums.type import MsgReturn
from api.services import scheduling_services as services
from api.models.dto.scheduling_dto import Scheduling


router = APIRouter(prefix="/book", tags=["book"])

@router.post("/",
    response_model = Scheduling,
    response_model_exclude_unset = True,
    responses = {
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
def create_Scheduling(scheduling: Scheduling, db: Session = Depends(get_db)):
    return services.create_scheduling(scheduling, db)


@router.get("/",
            response_model=List[Scheduling],
            response_model_exclude_unset=True,
            responses={
                200: {
                    "model": List[Scheduling],
                    "description": "Lista de Books",
                }
            },
            )
def get_all_scheduling(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return services.get_all_schedulings(skip, limit, db)

@router.get("/{scheduling_id}",
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

                }
            },
            )
def get_one_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.get_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.delete("/delete/{scheduling_id}",
               response_model= MsgReturn,
               response_model_exclude_unset=True,
               responses={
                   200: {
                       "model": MsgReturn,
                       "description": "Book excluido",
                   },
                   404: {
                       "model": GenericError,
                       "description": "Book Não Encontrado",

                   }
               },
               )
def delete_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.delete_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.put("/restore/{scheduling_id}",
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

                }
            },
            )
def restore_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.restore_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.put("/update/{scheduling_id}",
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

                }
            },
            )
def update_scheduling(scheduling_id: int, scheduling: Scheduling, db: Session = Depends(get_db)):
    try:
        return services.update_scheduling(db, scheduling_id, scheduling)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )