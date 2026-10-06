from django.db import models

# Create your models here.
from escuelas.models import Escuela

class Categoria(models.Model):
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=50, help_text="Ej: Sub-10, Sub-12, Sub-15")
    edad_minima = models.PositiveIntegerField()
    edad_maxima = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.edad_minima}-{self.edad_maxima} años) - {self.escuela.nombre}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['edad_minima']