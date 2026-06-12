from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EstudianteViewSet

router = DefaultRouter()
router.register("", EstudianteViewSet, basename="estudiante")

urlpatterns = [path("", include(router.urls))]
