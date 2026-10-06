from django.db import models

# Create your models here.
from usuarios.models import Usuario
from categorias.models import Categoria

class Entrenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'entrenador'})
    telefono = models.CharField(max_length=20, blank=True)
    categorias = models.ManyToManyField(Categoria, related_name='entrenadores')
    especialidad = models.CharField(max_length=100, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = "Entrenador"
        verbose_name_plural = "Entrenadores"