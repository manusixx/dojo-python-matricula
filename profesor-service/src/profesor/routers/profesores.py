from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from profesor import crud, schemas
from profesor.database import get_db
from profesor.exceptions import BusinessError, ResourceNotFoundError

# prefix: todas las rutas de este router empiezan con /api/v1/profesores
# tags: agrupa los endpoints en la documentación Swagger
router = APIRouter(prefix="/api/v1/profesores", tags=["Profesores"])


# HTTP POST → Crear un nuevo profesor
@router.post(
    "",
    response_model=schemas.ProfesorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un profesor",
)
def crear(
    data: schemas.ProfesorCreate,  # FastAPI valida automáticamente el body
    db: Session = Depends(get_db),  # Inyección de dependencia de la sesión BD
) -> schemas.ProfesorResponse:
    """Crea un nuevo profesor. Retorna 409 si email o identificación ya existen."""
    try:
        return schemas.ProfesorResponse.model_validate(crud.crear_profesor(db, data))
    except BusinessError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


# HTTP GET → Listar todos los profesores
@router.get("", response_model=list[schemas.ProfesorResponse], summary="Listar profesores")
def listar(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[schemas.ProfesorResponse]:
    """Retorna la lista de todos los profesores registrados."""
    return [
        schemas.ProfesorResponse.model_validate(p) for p in crud.obtener_profesores(db, skip, limit)
    ]


# HTTP GET → Obtener un profesor por id
@router.get("/{profesor_id}", response_model=schemas.ProfesorResponse, summary="Obtener profesor")
def obtener(
    profesor_id: int,
    db: Session = Depends(get_db),
) -> schemas.ProfesorResponse:
    """Retorna un profesor por su id. Retorna 404 si no existe."""
    try:
        return schemas.ProfesorResponse.model_validate(crud.obtener_profesor(db, profesor_id))
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


# HTTP PUT → Actualizar un profesor
@router.put(
    "/{profesor_id}", response_model=schemas.ProfesorResponse, summary="Actualizar profesor"
)
def actualizar(
    profesor_id: int,
    data: schemas.ProfesorUpdate,
    db: Session = Depends(get_db),
) -> schemas.ProfesorResponse:
    """Actualiza los campos enviados. Los campos no enviados no se modifican."""
    try:
        return schemas.ProfesorResponse.model_validate(
            crud.actualizar_profesor(db, profesor_id, data)
        )
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


# HTTP DELETE → Eliminar un profesor
@router.delete(
    "/{profesor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar profesor",
)
def eliminar(
    profesor_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Elimina un profesor. Retorna 204 No Content si tuvo éxito, 404 si no existe."""
    try:
        crud.eliminar_profesor(db, profesor_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
