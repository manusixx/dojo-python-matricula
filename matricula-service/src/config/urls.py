from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.views import health

urlpatterns = [
    # Endpoint de salud
    path("matricula-service/health/", health, name="health"),
    # Swagger: schema JSON y UI visual
    path("matricula-service/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "matricula-service/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Rutas de las apps
    path("api/v1/estudiantes/", include("estudiantes.urls")),
    path("api/v1/cursos/", include("cursos.urls")),
]
