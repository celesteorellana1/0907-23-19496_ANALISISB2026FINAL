from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, services
from app.database import get_db

router = APIRouter(
    prefix="/api/incidentes",
    tags=["Incidentes"]
)


@router.post("", response_model=schemas.IncidenteOut)
def crear_incidente(
    data: schemas.IncidenteCreate,
    db: Session = Depends(get_db),
):
    return services.crear_incidente(db, data)


@router.get("", response_model=list[schemas.IncidenteOut])
def listar_incidentes(
    db: Session = Depends(get_db),
):
    return services.listar_incidentes(db)


@router.post("/verificar-escalamientos")
def verificar_escalamientos(
    db: Session = Depends(get_db),
):
    total = services.verificar_escalamientos(db)

    return {
        "mensaje": "Verificación realizada correctamente.",
        "incidentes_escalados": total,
    }


@router.get("/{incidente_id}", response_model=schemas.IncidenteOut)
def obtener_incidente(
    incidente_id: int,
    db: Session = Depends(get_db),
):
    return services.obtener_incidente(db, incidente_id)


@router.put("/{incidente_id}/asignar", response_model=schemas.IncidenteOut)
def asignar_incidente(
    incidente_id: int,
    data: schemas.AsignarIncidente,
    db: Session = Depends(get_db),
):
    return services.asignar_incidente(db, incidente_id, data)


@router.put("/{incidente_id}/estado", response_model=schemas.IncidenteOut)
def cambiar_estado(
    incidente_id: int,
    data: schemas.CambiarEstado,
    db: Session = Depends(get_db),
):
    return services.cambiar_estado(db, incidente_id, data)


@router.put("/{incidente_id}/reasignar", response_model=schemas.IncidenteOut)
def reasignar_incidente(
    incidente_id: int,
    data: schemas.ReasignarIncidente,
    db: Session = Depends(get_db),
):
    return services.reasignar_incidente(db, incidente_id, data)


@router.get("/{incidente_id}/historial", response_model=list[schemas.HistorialOut])
def obtener_historial(
    incidente_id: int,
    db: Session = Depends(get_db),
):
    return services.obtener_historial(db, incidente_id)