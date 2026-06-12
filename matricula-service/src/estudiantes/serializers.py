from rest_framework import serializers

from .models import Estudiante


class EstudianteSerializer(serializers.ModelSerializer[Estudiante]):
    """
    Serializer completo para crear, actualizar y leer estudiantes.
    ModelSerializer infiere automáticamente los campos del modelo Django.
    """

    class Meta:
        model = Estudiante
        fields = "__all__"  # Incluye todos los campos del modelo

    def validate_semestre(self, value: int) -> int:
        """Validación adicional: el semestre debe estar entre 1 y 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError("El semestre debe estar entre 1 y 10.")
        return value
