from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from profesor import models, schemas
from profesor.exceptions import BusinessError, ResourceNotFoundError


def crear_profesor(db: Session, data: schemas.ProfesorCreate) -> models.Profesor:
    """Crea un profesor validando que email e identificación sean únicos."""
    # Verificar unicidad ANTES de insertar para dar un mensaje de error claro
    if db.query(models.Profesor).filter_by(email=data.email).first():
        raise BusinessError(f"Ya existe un profesor con email: {data.email}")
    if db.query(models.Profesor).filter_by(identificacion=data.identificacion).first():
        raise BusinessError(f"Ya existe un profesor con identificación: {data.identificacion}")
    profesor = models.Profesor(**data.model_dump())
    db.add(profesor)
    try:
        db.commit()
        db.refresh(profesor)  # Recarga el objeto con el id asignado por la BD
    except IntegrityError as e:
        db.rollback()
        raise BusinessError("Error de integridad en la base de datos") from e
    return profesor


def obtener_profesores(db: Session, skip: int = 0, limit: int = 100) -> list[models.Profesor]:
    """Retorna todos los profesores con paginación."""
    return db.query(models.Profesor).offset(skip).limit(limit).all()


def obtener_profesor(db: Session, profesor_id: int) -> models.Profesor:
    """Busca un profesor por id. Lanza ResourceNotFoundException si no existe."""
    profesor = db.query(models.Profesor).filter_by(id=profesor_id).first()
    if not profesor:
        raise ResourceNotFoundError(f"Profesor con id {profesor_id} no encontrado")
    return profesor


def actualizar_profesor(
    db: Session, profesor_id: int, data: schemas.ProfesorUpdate
) -> models.Profesor:
    """Actualiza solo los campos enviados en el body (PATCH semántico)."""
    profesor = obtener_profesor(db, profesor_id)
    # exclude_unset=True: solo procesa los campos que el cliente realmente envió
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profesor, key, value)
    db.commit()
    db.refresh(profesor)
    return profesor


def eliminar_profesor(db: Session, profesor_id: int) -> None:
    """Elimina un profesor. Lanza ResourceNotFoundException si no existe."""
    profesor = obtener_profesor(db, profesor_id)
    db.delete(profesor)
    db.commit()
