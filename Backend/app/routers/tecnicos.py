from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db

router = APIRouter(
    prefix="/api/tecnicos",
    tags=["Técnicos"]
)


@router.post("", response_model=schemas.TecnicoOut)
def crear_tecnico(
    data: schemas.TecnicoCreate,
    db: Session = Depends(get_db),
):
    return services.crear_tecnico(db, data)


@router.get("", response_model=list[schemas.TecnicoOut])
def listar_tecnicos(
    db: Session = Depends(get_db),
):
    return services.listar_tecnicos(db)