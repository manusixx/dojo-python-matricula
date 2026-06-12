from django.core.validators import MinValueValidator
from django.db import models

from estudiantes.models import Estudiante


class Curso(models.Model):
    """Modelo Django para la tabla cursos."""

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    creditos = models.IntegerField(validators=[MinValueValidator(1)])

    # profesor_id referencia un registro de la tabla 'profesores', que pertenece
    # al profesor-service (FastAPI + SQLAlchemy). No usamos ForeignKey de Django
    # porque el modelo Profesor no existe dentro de este proyecto Django.
    profesor_id = models.IntegerField()

    # Relación muchos a muchos con Estudiante: representa la matrícula.
    # Django crea automáticamente la tabla intermedia cursos_curso_estudiantes.
    estudiantes = models.ManyToManyField(Estudiante, related_name="cursos", blank=True)

    class Meta:
        db_table = "cursos"
        ordering = ["codigo"]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"
