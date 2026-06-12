import pytest
from rest_framework.test import APIClient

DATA = {
    "nombre": "Laura",
    "apellido": "Gomez",
    "email": "laura.gomez@correounivalle.edu.co",
    "identificacion": "1144556677",
    "semestre": 5,
}


@pytest.mark.django_db
class TestEstudianteAPI:
    def test_crear_estudiante_retorna_201(self, api_client: APIClient) -> None:
        r = api_client.post("/api/v1/estudiantes/", DATA, format="json")
        assert r.status_code == 201
        assert r.data["email"] == DATA["email"]

    def test_crear_email_duplicado_retorna_400(self, api_client: APIClient) -> None:
        api_client.post("/api/v1/estudiantes/", DATA, format="json")
        r = api_client.post("/api/v1/estudiantes/", DATA, format="json")
        assert r.status_code == 400

    def test_listar_estudiantes_retorna_200(self, api_client: APIClient) -> None:
        r = api_client.get("/api/v1/estudiantes/")
        assert r.status_code == 200
        assert isinstance(r.data, list)

    def test_obtener_por_id_retorna_200(self, api_client: APIClient) -> None:
        creado = api_client.post("/api/v1/estudiantes/", DATA, format="json").data
        r = api_client.get(f"/api/v1/estudiantes/{creado['id']}/")
        assert r.status_code == 200

    def test_obtener_id_inexistente_retorna_404(self, api_client: APIClient) -> None:
        r = api_client.get("/api/v1/estudiantes/999999/")
        assert r.status_code == 404

    def test_actualizar_retorna_200_con_datos_nuevos(self, api_client: APIClient) -> None:
        creado = api_client.post("/api/v1/estudiantes/", DATA, format="json").data
        r = api_client.put(
            f"/api/v1/estudiantes/{creado['id']}/",
            {**DATA, "nombre": "Laura Actualizada"},
            format="json",
        )
        assert r.status_code == 200
        assert r.data["nombre"] == "Laura Actualizada"

    def test_eliminar_retorna_204(self, api_client: APIClient) -> None:
        creado = api_client.post("/api/v1/estudiantes/", DATA, format="json").data
        r = api_client.delete(f"/api/v1/estudiantes/{creado['id']}/")
        assert r.status_code == 204

    def test_crear_con_semestre_invalido_retorna_400(self, api_client: APIClient) -> None:
        datos_invalidos = {
            **DATA,
            "identificacion": "0000000000",
            "email": "invalido@correounivalle.edu.co",
            "semestre": 11,
        }
        r = api_client.post("/api/v1/estudiantes/", datos_invalidos, format="json")
        assert r.status_code == 400
