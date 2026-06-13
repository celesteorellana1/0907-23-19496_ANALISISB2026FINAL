from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Especialidad(str, Enum):
    FIBRA_OPTICA = "fibra_optica"
    MICROONDAS = "microondas"
    SISTEMAS_ELECTRICOS = "sistemas_electricos"


class Severidad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"
    CRITICO = "critico"


class Estado(str, Enum):
    REGISTRADO = "Registrado"
    ASIGNADO = "Asignado"
    EN_PROGRESO = "En progreso"
    RESUELTO = "Resuelto"
    CERRADO = "Cerrado"


class TecnicoCreate(BaseModel):
    nombre: str
    especialidad: Especialidad


class TecnicoOut(BaseModel):
    id: int
    nombre: str
    especialidad: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class IncidenteCreate(BaseModel):
    sitio: str
    tipo_incidente: Especialidad
    severidad: Severidad
    descripcion: str


class IncidenteOut(BaseModel):
    id: int
    sitio: str
    tipo_incidente: str
    severidad: str
    descripcion: str
    estado: str
    escalado: bool
    fecha_creacion: datetime
    fecha_asignacion: Optional[datetime]
    fecha_cierre: Optional[datetime]
    tecnico_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AsignarIncidente(BaseModel):
    tecnico_id: int


class CambiarEstado(BaseModel):
    nuevo_estado: Estado


class ReasignarIncidente(BaseModel):
    nuevo_tecnico_id: int


class HistorialOut(BaseModel):
    id: int
    incidente_id: int
    accion: str
    estado_anterior: Optional[str]
    estado_nuevo: Optional[str]
    tecnico_anterior_id: Optional[int]
    tecnico_nuevo_id: Optional[int]
    detalle: Optional[str]
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)