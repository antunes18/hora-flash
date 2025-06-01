from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.models.scheduling import Scheduling
from api.services import scheduling_services as services
from api.models.dto.scheduling_dto import Scheduling


router = APIRouter(prefix="/book", tags=["book"])

@router.post("/")
def create_Scheduling(scheduling: Scheduling, db: Session = Depends(get_db)):
    try:
        return services.create_scheduling(scheduling, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
def get_all_scheduling(db: Session = Depends(get_db)):
    try:
        return services.get_all_schedulings(db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{scheduling_id}")
def get_one_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.get_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.delete("/delete/{scheduling_id}")
def delete_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.delete_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.put("/restore/{scheduling_id}")
def restore_scheduling(scheduling_id: int, db: Session = Depends(get_db)):
    try:
        return services.restore_scheduling(db, scheduling_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.put("/update/{scheduling_id}")
def update_scheduling(scheduling_id: int, scheduling: Scheduling, db: Session = Depends(get_db)):
    try:
        return services.update_scheduling(db, scheduling_id, scheduling)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )