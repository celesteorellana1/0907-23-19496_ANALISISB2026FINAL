from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import incidentes, tecnicos, reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NetGuard GT API",
    description="API REST para gestión de incidentes de red.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API REST NetGuard GT funcionando correctamente."
    }


app.include_router(tecnicos.router)
app.include_router(incidentes.router)
app.include_router(reportes.router)