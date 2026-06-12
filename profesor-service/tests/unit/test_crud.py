import pytest
from sqlalchemy.orm import Session

from profesor.crud import (
    actualizar_profesor,
    crear_profesor,
    eliminar_profesor,
    obtener_profesor,
    obtener_profesores,
)
from profesor.exceptions import BusinessError, ResourceNotFoundError
from profesor.schemas import ProfesorCreate, ProfesorUpdate


def _datos_validos(**overrides: str) -> ProfesorCreate:
    """Helper: construye datos de prueba válidos con valores por defecto."""
    defaults = {
        "nombre": "Carlos",
        "apellido": "Ramirez",
        "email": "carlos@univalle.edu.co",
        "identificacion": "12345678",
    }
    defaults.update(overrides)
    return ProfesorCreate(**defaults)


class TestCrearProfesor:
    def test_crear_con_datos_validos_retorna_profesor(self, db_session: Session) -> None:
        profesor = crear_profesor(db_session, _datos_validos())
        assert profesor.id is not None
        assert profesor.email == "carlos@univalle.edu.co"

    def test_crear_con_email_duplicado_lanza_business_exception(self, db_session: Session) -> None:
        crear_profesor(db_session, _datos_validos())
        with pytest.raises(BusinessError):
            crear_profesor(db_session, _datos_validos(identificacion="99999999"))

    def test_crear_con_identificacion_duplicada_lanza_business_exception(
        self, db_session: Session
    ) -> None:
        crear_profesor(db_session, _datos_validos())
        with pytest.raises(BusinessError):
            crear_profesor(db_session, _datos_validos(email="otro@univalle.edu.co"))


class TestObtenerProfesor:
    def test_obtener_por_id_existente_retorna_profesor(self, db_session: Session) -> None:
        creado = crear_profesor(db_session, _datos_validos())
        encontrado = obtener_profesor(db_session, creado.id)
        assert encontrado.id == creado.id

    def test_obtener_id_inexistente_lanza_not_found(self, db_session: Session) -> None:
        with pytest.raises(ResourceNotFoundError):
            obtener_profesor(db_session, 999)

    def test_obtener_todos_retorna_lista_completa(self, db_session: Session) -> None:
        crear_profesor(db_session, _datos_validos())
        crear_profesor(
            db_session, _datos_validos(email="otro@univalle.edu.co", identificacion="99999")
        )
        assert len(obtener_profesores(db_session)) == 2


class TestActualizarProfesor:
    def test_actualizar_nombre_retorna_datos_actualizados(self, db_session: Session) -> None:
        creado = crear_profesor(db_session, _datos_validos())
        actualizado = actualizar_profesor(
            db_session, creado.id, ProfesorUpdate(nombre="Carlos Nuevo")
        )
        assert actualizado.nombre == "Carlos Nuevo"

    def test_actualizar_id_inexistente_lanza_not_found(self, db_session: Session) -> None:
        with pytest.raises(ResourceNotFoundError):
            actualizar_profesor(db_session, 999, ProfesorUpdate(nombre="XYZ"))


class TestEliminarProfesor:
    def test_eliminar_existente_lo_borra_de_la_bd(self, db_session: Session) -> None:
        creado = crear_profesor(db_session, _datos_validos())
        eliminar_profesor(db_session, creado.id)
        with pytest.raises(ResourceNotFoundError):
            obtener_profesor(db_session, creado.id)

    def test_eliminar_id_inexistente_lanza_not_found(self, db_session: Session) -> None:
        with pytest.raises(ResourceNotFoundError):
            eliminar_profesor(db_session, 999)
