from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.models.scheduling import Scheduling
from api.services import scheduling_services as services
from api.models.dto.scheduling_dto import Scheduling


router = APIRouter(prefix="/book", tags=["book"])

@router.post("/", response_model=None)
def create_Scheduling(scheduling: Scheduling, db: Session = Depends(get_db)):
    try:
        return services.create_scheduling(scheduling, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
