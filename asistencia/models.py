from django.db import models

# Create your models here.
from entrenamientos.models import Entrenamiento
from jugadores.models import Jugador

class Asistencia(models.Model):
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE, related_name='asistencias')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='asistencias')
    presente = models.BooleanField(default=False)
    observacion = models.CharField(max_length=200, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Presente" if self.presente else "Ausente"
        return f"{self.jugador.nombre_completo} - {self.entrenamiento.fecha} - {estado}"

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        unique_together = ('entrenamiento', 'jugador')