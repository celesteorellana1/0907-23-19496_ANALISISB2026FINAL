from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db

router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes"]
)


@router.get("/incidentes")
def reporte_incidentes(
    db: Session = Depends(get_db),
):
    return services.generar_reporte_incidentes(db)