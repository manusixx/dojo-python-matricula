from typing import Any

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Curso
from .serializers import CursoSerializer


class CursoViewSet(viewsets.ModelViewSet[Curso]):
    """CRUD completo para Curso."""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
