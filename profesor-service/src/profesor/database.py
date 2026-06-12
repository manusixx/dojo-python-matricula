from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from profesor.config import settings

# Equivalente al DataSource de Spring Boot
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Fábrica de sesiones — equivalente a la inyección del EntityManager
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos ORM."""


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia FastAPI: abre una sesión de BD, la entrega al endpoint
    y la cierra al terminar — incluso si hay un error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
