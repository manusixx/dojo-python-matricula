import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Cliente HTTP de pruebas para los endpoints REST de Django."""
    return APIClient()
