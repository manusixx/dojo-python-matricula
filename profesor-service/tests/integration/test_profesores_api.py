import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from profesor.database import Base, get_db
from profesor.main import app


@pytest.fixture(scope="module")
def postgres_engine():
    """
    Levanta un contenedor PostgreSQL real una sola vez para todo el módulo.
    Crea las tablas al inicio y las elimina al finalizar todos los tests.
    """
    with PostgresContainer("postgres:16-alpine") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(bind=engine)
        yield engine
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def postgres_client(postgres_engine):
    """Cliente HTTP de prueba conectado al PostgreSQL del contenedor."""
    session = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)

    def override_get_db():
        db = session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def limpiar_bd(postgres_engine):
    """
    Se ejecuta automáticamente ANTES de cada test (autouse=True).
    Vacía la tabla profesores para que cada test parta de una BD limpia,
    igual que el @BeforeEach limpiarBaseDeDatos() del dojo Java.
    """
    with postgres_engine.begin() as conn:
        conn.execute(text("DELETE FROM profesores"))


# Datos de prueba reutilizables en todos los tests
DATA = {
    "nombre": "Ana",
    "apellido": "Lopez",
    "email": "ana.lopez@univalle.edu.co",
    "identificacion": "87654321",
}


class TestProfesorAPIIntegracion:
    def test_crear_profesor_retorna_201(self, postgres_client: TestClient) -> None:
        r = postgres_client.post("/api/v1/profesores", json=DATA)
        assert r.status_code == 201
        assert r.json()["email"] == DATA["email"]

    def test_crear_email_duplicado_retorna_409(self, postgres_client: TestClient) -> None:
        postgres_client.post("/api/v1/profesores", json=DATA)
        r = postgres_client.post("/api/v1/profesores", json=DATA)
        assert r.status_code == 409

    def test_listar_profesores_retorna_200(self, postgres_client: TestClient) -> None:
        r = postgres_client.get("/api/v1/profesores")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_obtener_por_id_retorna_200(self, postgres_client: TestClient) -> None:
        creado = postgres_client.post("/api/v1/profesores", json=DATA).json()
        r = postgres_client.get(f"/api/v1/profesores/{creado['id']}")
        assert r.status_code == 200

    def test_obtener_id_inexistente_retorna_404(self, postgres_client: TestClient) -> None:
        r = postgres_client.get("/api/v1/profesores/999999")
        assert r.status_code == 404

    def test_actualizar_retorna_200_con_datos_nuevos(self, postgres_client: TestClient) -> None:
        creado = postgres_client.post("/api/v1/profesores", json=DATA).json()
        r = postgres_client.put(f"/api/v1/profesores/{creado['id']}", json={"nombre": "Ana Nueva"})
        assert r.status_code == 200
        assert r.json()["nombre"] == "Ana Nueva"

    def test_eliminar_retorna_204(self, postgres_client: TestClient) -> None:
        creado = postgres_client.post("/api/v1/profesores", json=DATA).json()
        r = postgres_client.delete(f"/api/v1/profesores/{creado['id']}")
        assert r.status_code == 204
