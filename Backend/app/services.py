from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas


FLUJO_ESTADOS = [
    schemas.Estado.REGISTRADO.value,
    schemas.Estado.ASIGNADO.value,
    schemas.Estado.EN_PROGRESO.value,
    schemas.Estado.RESUELTO.value,
    schemas.Estado.CERRADO.value,
]

ESTADOS_ACTIVOS = [
    schemas.Estado.ASIGNADO.value,
    schemas.Estado.EN_PROGRESO.value,
]

SEVERIDADES_ESCALABLES = [
    schemas.Severidad.CRITICO.value,
    schemas.Severidad.URGENTE.value,
]

SLA_HORAS = {
    schemas.Severidad.CRITICO.value: 4,
    schemas.Severidad.URGENTE.value: 8,
    schemas.Severidad.ALTA.value: 24,
    schemas.Severidad.MEDIA.value: 48,
    schemas.Severidad.BAJA.value: 72,
}


def registrar_historial(
    db: Session,
    incidente_id: int,
    accion: str,
    estado_anterior: str | None = None,
    estado_nuevo: str | None = None,
    tecnico_anterior_id: int | None = None,
    tecnico_nuevo_id: int | None = None,
    detalle: str | None = None,
):
    historial = models.HistorialIncidente(
        incidente_id=incidente_id,
        accion=accion,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,
        tecnico_anterior_id=tecnico_anterior_id,
        tecnico_nuevo_id=tecnico_nuevo_id,
        detalle=detalle,
    )

    db.add(historial)
    db.flush()


def crear_tecnico(db: Session, data: schemas.TecnicoCreate):
    tecnico = models.Tecnico(
        nombre=data.nombre,
        especialidad=data.especialidad.value,
    )

    db.add(tecnico)
    db.commit()
    db.refresh(tecnico)

    return tecnico


def listar_tecnicos(db: Session):
    return db.query(models.Tecnico).all()


def crear_incidente(db: Session, data: schemas.IncidenteCreate):
    incidente = models.Incidente(
        sitio=data.sitio,
        tipo_incidente=data.tipo_incidente.value,
        severidad=data.severidad.value,
        descripcion=data.descripcion,
        estado=schemas.Estado.REGISTRADO.value,
        escalado=False,
    )

    db.add(incidente)
    db.flush()

    registrar_historial(
        db=db,
        incidente_id=incidente.id,
        accion="CREACION",
        estado_anterior=None,
        estado_nuevo=schemas.Estado.REGISTRADO.value,
        detalle="Incidente registrado correctamente.",
    )

    db.commit()
    db.refresh(incidente)

    return incidente


def obtener_incidente(db: Session, incidente_id: int):
    incidente = db.query(models.Incidente).filter(
        models.Incidente.id == incidente_id
    ).first()

    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado.")

    fue_escalado = verificar_escalamiento_incidente(db, incidente)

    if fue_escalado:
        db.commit()
        db.refresh(incidente)

    return incidente


def listar_incidentes(db: Session):
    verificar_escalamientos(db)
    return db.query(models.Incidente).all()


def contar_incidentes_activos(db: Session, tecnico_id: int):
    return db.query(models.Incidente).filter(
        models.Incidente.tecnico_id == tecnico_id,
        models.Incidente.estado.in_(ESTADOS_ACTIVOS)
    ).count()


def validar_tecnico_para_incidente(
    db: Session,
    tecnico_id: int,
    incidente: models.Incidente,
):
    tecnico = db.query(models.Tecnico).filter(
        models.Tecnico.id == tecnico_id
    ).first()

    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado.")

    if not tecnico.activo:
        raise HTTPException(
            status_code=400,
            detail="El técnico no está activo."
        )

    if tecnico.especialidad != incidente.tipo_incidente:
        raise HTTPException(
            status_code=400,
            detail="La especialidad del técnico no coincide con el tipo de incidente."
        )

    activos = contar_incidentes_activos(db, tecnico.id)

    if incidente.tecnico_id != tecnico.id and activos >= 3:
        raise HTTPException(
            status_code=400,
            detail="El técnico ya tiene 3 incidentes activos."
        )

    return tecnico


def asignar_incidente(
    db: Session,
    incidente_id: int,
    data: schemas.AsignarIncidente,
):
    incidente = obtener_incidente(db, incidente_id)

    if incidente.estado != schemas.Estado.REGISTRADO.value:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden asignar incidentes en estado Registrado."
        )

    tecnico = validar_tecnico_para_incidente(
        db=db,
        tecnico_id=data.tecnico_id,
        incidente=incidente,
    )

    estado_anterior = incidente.estado

    incidente.tecnico_id = tecnico.id
    incidente.estado = schemas.Estado.ASIGNADO.value
    incidente.fecha_asignacion = datetime.utcnow()

    registrar_historial(
        db=db,
        incidente_id=incidente.id,
        accion="ASIGNACION",
        estado_anterior=estado_anterior,
        estado_nuevo=incidente.estado,
        tecnico_anterior_id=None,
        tecnico_nuevo_id=tecnico.id,
        detalle=f"Incidente asignado al técnico {tecnico.nombre}.",
    )

    db.commit()
    db.refresh(incidente)

    return incidente


def cambiar_estado(
    db: Session,
    incidente_id: int,
    data: schemas.CambiarEstado,
):
    incidente = obtener_incidente(db, incidente_id)

    estado_actual = incidente.estado
    estado_nuevo = data.nuevo_estado.value

    if estado_actual not in FLUJO_ESTADOS:
        raise HTTPException(
            status_code=400,
            detail="El estado actual del incidente no es válido."
        )

    indice_actual = FLUJO_ESTADOS.index(estado_actual)
    indice_nuevo = FLUJO_ESTADOS.index(estado_nuevo)

    if estado_nuevo == schemas.Estado.ASIGNADO.value:
        raise HTTPException(
            status_code=400,
            detail="Para pasar a Asignado use el endpoint de asignación."
        )

    if indice_nuevo != indice_actual + 1:
        raise HTTPException(
            status_code=400,
            detail="El estado solo puede avanzar en una dirección y sin saltarse pasos."
        )

    if estado_nuevo == schemas.Estado.EN_PROGRESO.value and incidente.tecnico_id is None:
        raise HTTPException(
            status_code=400,
            detail="No se puede iniciar un incidente sin técnico asignado."
        )

    incidente.estado = estado_nuevo

    if estado_nuevo == schemas.Estado.CERRADO.value:
        incidente.fecha_cierre = datetime.utcnow()

    registrar_historial(
        db=db,
        incidente_id=incidente.id,
        accion="CAMBIO_ESTADO",
        estado_anterior=estado_actual,
        estado_nuevo=estado_nuevo,
        tecnico_anterior_id=incidente.tecnico_id,
        tecnico_nuevo_id=incidente.tecnico_id,
        detalle=f"Estado cambiado de {estado_actual} a {estado_nuevo}.",
    )

    db.commit()
    db.refresh(incidente)

    return incidente


def reasignar_incidente(
    db: Session,
    incidente_id: int,
    data: schemas.ReasignarIncidente,
):
    incidente = obtener_incidente(db, incidente_id)

    if incidente.estado == schemas.Estado.CERRADO.value:
        raise HTTPException(
            status_code=400,
            detail="No se puede reasignar un incidente cerrado."
        )

    tecnico_anterior_id = incidente.tecnico_id

    if tecnico_anterior_id == data.nuevo_tecnico_id:
        raise HTTPException(
            status_code=400,
            detail="El incidente ya está asignado a ese técnico."
        )

    nuevo_tecnico = validar_tecnico_para_incidente(
        db=db,
        tecnico_id=data.nuevo_tecnico_id,
        incidente=incidente,
    )

    incidente.tecnico_id = nuevo_tecnico.id

    if incidente.estado == schemas.Estado.REGISTRADO.value:
        incidente.estado = schemas.Estado.ASIGNADO.value
        incidente.fecha_asignacion = datetime.utcnow()

    registrar_historial(
        db=db,
        incidente_id=incidente.id,
        accion="REASIGNACION",
        estado_anterior=incidente.estado,
        estado_nuevo=incidente.estado,
        tecnico_anterior_id=tecnico_anterior_id,
        tecnico_nuevo_id=nuevo_tecnico.id,
        detalle=f"Incidente reasignado al técnico {nuevo_tecnico.nombre}.",
    )

    db.commit()
    db.refresh(incidente)

    return incidente


def verificar_escalamiento_incidente(
    db: Session,
    incidente: models.Incidente,
):
    limite = datetime.utcnow() - timedelta(hours=2)

    if (
        incidente.severidad in SEVERIDADES_ESCALABLES
        and incidente.estado == schemas.Estado.REGISTRADO.value
        and not incidente.escalado
        and incidente.fecha_creacion <= limite
    ):
        incidente.escalado = True

        registrar_historial(
            db=db,
            incidente_id=incidente.id,
            accion="ESCALAMIENTO",
            estado_anterior=incidente.estado,
            estado_nuevo=incidente.estado,
            tecnico_anterior_id=incidente.tecnico_id,
            tecnico_nuevo_id=incidente.tecnico_id,
            detalle="Incidente crítico o urgente escalado automáticamente por superar 2 horas sin atención.",
        )

        return True

    return False


def verificar_escalamientos(db: Session):
    incidentes = db.query(models.Incidente).filter(
        models.Incidente.estado == schemas.Estado.REGISTRADO.value,
        models.Incidente.escalado == False,
        models.Incidente.severidad.in_(SEVERIDADES_ESCALABLES),
    ).all()

    total = 0

    for incidente in incidentes:
        if verificar_escalamiento_incidente(db, incidente):
            total += 1

    if total > 0:
        db.commit()

    return total


def obtener_historial(db: Session, incidente_id: int):
    obtener_incidente(db, incidente_id)

    return db.query(models.HistorialIncidente).filter(
        models.HistorialIncidente.incidente_id == incidente_id
    ).order_by(models.HistorialIncidente.fecha.asc()).all()


def generar_reporte_incidentes(db: Session):
    verificar_escalamientos(db)

    total_incidentes = db.query(models.Incidente).count()

    por_estado = db.query(
        models.Incidente.estado,
        func.count(models.Incidente.id)
    ).group_by(models.Incidente.estado).all()

    por_severidad = db.query(
        models.Incidente.severidad,
        func.count(models.Incidente.id)
    ).group_by(models.Incidente.severidad).all()

    por_tecnico = db.query(
        models.Tecnico.nombre,
        func.count(models.Incidente.id)
    ).join(
        models.Incidente,
        models.Tecnico.id == models.Incidente.tecnico_id
    ).group_by(models.Tecnico.nombre).all()

    escalados = db.query(models.Incidente).filter(
        models.Incidente.escalado == True
    ).count()

    return {
        "total_incidentes": total_incidentes,
        "incidentes_escalados": escalados,
        "por_estado": [
            {"estado": estado, "cantidad": cantidad}
            for estado, cantidad in por_estado
        ],
        "por_severidad": [
            {"severidad": severidad, "cantidad": cantidad}
            for severidad, cantidad in por_severidad
        ],
        "por_tecnico": [
            {"tecnico": tecnico, "cantidad": cantidad}
            for tecnico, cantidad in por_tecnico
        ],
        "sla_horas_por_severidad": SLA_HORAS,
    }