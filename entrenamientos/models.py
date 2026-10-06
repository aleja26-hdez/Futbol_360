from django.db import models

# Create your models here.
from categorias.models import Categoria
from entrenadores.models import Entrenador

class Entrenamiento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='entrenamientos')
    entrenador = models.ForeignKey(Entrenador, on_delete=models.SET_NULL, null=True, related_name='entrenamientos')

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=150)
    tema = models.CharField(max_length=150, blank=True, help_text="Ej: Técnica de pase, resistencia física")

    def __str__(self):
        return f"{self.categoria.nombre} - {self.fecha} ({self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')})"

    class Meta:
        verbose_name = "Entrenamiento"
        verbose_name_plural = "Entrenamientos"
        ordering = ['-fecha', 'hora_inicio']