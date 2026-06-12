from rest_framework import serializers

from .models import Curso


class CursoSerializer(serializers.ModelSerializer[Curso]):
    """Serializer completo para crear, actualizar y leer cursos."""

    class Meta:
        model = Curso
        fields = ["id", "codigo", "nombre", "creditos", "profesor_id", "estudiantes"]
        # estudiantes (la matrícula) se gestiona con endpoints dedicados,
        # no en el create/update directo
        read_only_fields = ["estudiantes"]
