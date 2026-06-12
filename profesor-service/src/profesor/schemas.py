from pydantic import BaseModel, EmailStr, Field


class ProfesorBase(BaseModel):
    """Campos comunes que comparten los schemas de creación y respuesta."""

    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr  # Valida automáticamente que sea un email válido
    identificacion: str = Field(..., min_length=5, max_length=50)


class ProfesorCreate(ProfesorBase):
    """Schema de entrada para crear un profesor (POST /api/v1/profesores)."""

    # Hereda todos los campos de ProfesorBase sin cambios


class ProfesorUpdate(BaseModel):
    """Schema de entrada para actualizar un profesor (PUT /api/v1/profesores/{id}).
    Todos los campos son opcionales: solo se actualizan los que se envíen.
    """

    nombre: str | None = Field(None, min_length=2, max_length=100)
    apellido: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    identificacion: str | None = Field(None, min_length=5, max_length=50)


class ProfesorResponse(ProfesorBase):
    """Schema de salida: incluye el id asignado por la BD.
    Equivalente al @ResponseBody con DTO de salida en Spring Boot.
    """

    id: int

    # from_attributes=True permite convertir un objeto ORM (Profesor) a este schema
    model_config = {"from_attributes": True}
