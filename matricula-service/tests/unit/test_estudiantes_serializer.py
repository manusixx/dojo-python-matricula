import pytest

from estudiantes.serializers import EstudianteSerializer

VALID_DATA = {
    "nombre": "Laura",
    "apellido": "Gomez",
    "email": "laura.gomez@correounivalle.edu.co",
    "identificacion": "1144556677",
    "semestre": 5,
}


@pytest.mark.django_db
class TestEstudianteSerializer:
    """
    Tests unitarios: validan la lógica del Serializer directamente,
    sin pasar por HTTP ni por el ViewSet.

    Nota: usan @pytest.mark.django_db porque los campos unique=True
    (email, identificacion) generan un UniqueValidator que consulta la BD.
    """

    def test_datos_validos_es_valido(self) -> None:
        serializer = EstudianteSerializer(data=VALID_DATA)
        assert serializer.is_valid()

    def test_semestre_menor_a_uno_no_es_valido(self) -> None:
        data = {
            **VALID_DATA,
            "identificacion": "0000000001",
            "email": "a@correounivalle.edu.co",
            "semestre": 0,
        }
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert "semestre" in serializer.errors

    def test_semestre_mayor_a_diez_no_es_valido(self) -> None:
        data = {
            **VALID_DATA,
            "identificacion": "0000000002",
            "email": "b@correounivalle.edu.co",
            "semestre": 11,
        }
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert "semestre" in serializer.errors

    def test_email_con_formato_invalido_no_es_valido(self) -> None:
        data = {**VALID_DATA, "identificacion": "0000000003", "email": "no-es-un-email"}
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
