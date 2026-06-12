from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from profesor.database import Base


class Profesor(Base):
    """
    Modelo ORM que mapea a la tabla 'profesores' en PostgreSQL.
    Equivalente a @Entity @Table(name='profesores') en Java.
    """

    __tablename__ = "profesores"

    # Clave primaria autoincremental
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # String(100) equivale a VARCHAR(100) en la BD
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)

    # unique=True garantiza que no haya dos profesores con el mismo email
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    identificacion: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
