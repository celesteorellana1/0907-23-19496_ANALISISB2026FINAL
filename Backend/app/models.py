from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    incidentes = relationship("Incidente", back_populates="tecnico")


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    sitio = Column(String, nullable=False)
    tipo_incidente = Column(String, nullable=False)
    severidad = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)

    estado = Column(String, default="Registrado")
    escalado = Column(Boolean, default=False)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_asignacion = Column(DateTime, nullable=True)
    fecha_cierre = Column(DateTime, nullable=True)

    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)

    tecnico = relationship("Tecnico", back_populates="incidentes")
    historial = relationship("HistorialIncidente", back_populates="incidente")


class HistorialIncidente(Base):
    __tablename__ = "historial_incidentes"

    id = Column(Integer, primary_key=True, index=True)

    incidente_id = Column(Integer, ForeignKey("incidentes.id"), nullable=False)

    accion = Column(String, nullable=False)
    estado_anterior = Column(String, nullable=True)
    estado_nuevo = Column(String, nullable=True)

    tecnico_anterior_id = Column(Integer, nullable=True)
    tecnico_nuevo_id = Column(Integer, nullable=True)

    detalle = Column(Text, nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    incidente = relationship("Incidente", back_populates="historial")