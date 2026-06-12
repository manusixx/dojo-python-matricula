from fastapi import FastAPI

from profesor.database import Base, engine
from profesor.routers import profesores

# Crear la instancia de la aplicación FastAPI
# docs_url: ruta donde estará disponible el Swagger UI
app = FastAPI(
    title="Profesor Service",
    description="Microservicio de gestión de profesores — Matrícula Académica",
    version="1.0.0",
    docs_url="/profesor-service/docs",
    redoc_url="/profesor-service/redoc",
    openapi_url="/profesor-service/openapi.json",
)

# Crear las tablas en la BD al iniciar la app
# En producción, Alembic gestiona las migraciones en lugar de este comando
Base.metadata.create_all(bind=engine)

# Registrar el router de profesores
app.include_router(profesores.router)


@app.get("/profesor-service/health")
def health() -> dict[str, str]:
    """Endpoint de salud — usado por el pipeline CD para verificar el despliegue."""
    return {"status": "UP", "service": "profesor-service"}
