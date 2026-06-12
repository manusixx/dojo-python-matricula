from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CursoViewSet

router = DefaultRouter()
router.register("", CursoViewSet, basename="curso")

urlpatterns = [path("", include(router.urls))]
