from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Estudiante(models.Model):
    """
    Modelo Django para la tabla estudiantes.
    No necesitas definir @Entity ni @Column — Django lo gestiona.
    """

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    identificacion = models.CharField(max_length=50, unique=True)
    semestre = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        db_table = "estudiantes"
        ordering = ["apellido", "nombre"]

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} ({self.email})"
