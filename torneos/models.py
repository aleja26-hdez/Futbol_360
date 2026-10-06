from django.db import models

# Create your models here.
from categorias.models import Categoria

class Torneo(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='torneos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Torneo"
        verbose_name_plural = "Torneos"
        ordering = ['-fecha_inicio']


class Partido(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidos')
    rival = models.CharField(max_length=150)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=150, blank=True)
    goles_favor = models.PositiveIntegerField(default=0)
    goles_contra = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.torneo.nombre} vs {self.rival} - {self.fecha} {self.hora.strftime('%H:%M')}"

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        ordering = ['fecha', 'hora']