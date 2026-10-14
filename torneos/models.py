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

class Cruce(models.Model):
    RONDAS = [('cuartos', 'Cuartos de final'), ('semis', 'Semifinales'), ('final', 'Final')]
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='cruces')
    ronda = models.CharField(max_length=10, choices=RONDAS)
    posicion = models.PositiveSmallIntegerField()  # cuartos 1-4, semis 1-2, final 1
    equipo_a = models.CharField(max_length=100, blank=True)  # solo se escriben en cuartos
    equipo_b = models.CharField(max_length=100, blank=True)
    goles_a = models.PositiveIntegerField(null=True, blank=True)
    goles_b = models.PositiveIntegerField(null=True, blank=True)
    penales_a = models.PositiveIntegerField(null=True, blank=True)
    penales_b = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('torneo', 'ronda', 'posicion')