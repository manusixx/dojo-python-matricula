from typing import Any

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Estudiante
from .serializers import EstudianteSerializer


class EstudianteViewSet(viewsets.ModelViewSet[Estudiante]):
    """
    CRUD completo para Estudiante.
    ModelViewSet genera automáticamente: GET /estudiantes/, GET /estudiantes/{id}/,
    POST /estudiantes/, PUT /estudiantes/{id}/, PATCH /estudiantes/{id}/,
    DELETE /estudiantes/{id}/
    """

    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Sobreescribimos create para retornar 201 Created explícitamente."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
