from django.http import HttpRequest, JsonResponse


def health(request: HttpRequest) -> JsonResponse:
    """Endpoint de salud — usado por el pipeline CD para verificar el despliegue."""
    return JsonResponse({"status": "UP", "service": "matricula-service"})
