from django.db import models

# Create your models here.
from categorias.models import Categoria
from usuarios.models import Usuario

class Jugador(models.Model):
    nombre_completo = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200, blank=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    acudiente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'padre'})
    telefono_acudiente = models.CharField(max_length=20, blank=True)

    fecha_inscripcion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    @property
    def edad(self):
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def __str__(self):
        return f"{self.nombre_completo} ({self.edad} años) - {self.categoria.nombre}"

    @property
    def total_asistencias(self):
        return self.asistencias.filter(presente=True).count()

    @property
    def total_faltas(self):
        return self.asistencias.filter(presente=False).count()