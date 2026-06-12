import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from profesor.database import Base, get_db
from profesor.main import app

# Motor SQLite en memoria para tests unitarios — no requiere Docker
ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Una sola conexión compartida — necesario para SQLite en memoria
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


@pytest.fixture(scope="function")
def db_session():
    """
    Crea y destruye las tablas para cada test unitario.
    Garantiza que cada test parte de una base de datos limpia.
    """
    Base.metadata.create_all(bind=ENGINE)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=ENGINE)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente HTTP de prueba con la BD en memoria inyectada.
    Equivalente al TestRestTemplate de Spring Boot.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
