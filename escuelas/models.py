from django.db import models

# Create your models here.

class Escuela(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)

    edad_minima = models.PositiveIntegerField(help_text="Edad mínima de los jugadores aceptados")
    edad_maxima = models.PositiveIntegerField(help_text="Edad máxima de los jugadores aceptados")

    telefono = models.CharField(max_length=20)
    instagram = models.URLField(blank=True, help_text="Link al perfil de Instagram")
    facebook = models.URLField(blank=True, help_text="Link a la página de Facebook")

    logo = models.ImageField(upload_to='escuelas/logos/', blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class FotoInstalacion(models.Model):
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='escuelas/instalaciones/')
    descripcion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Foto de {self.escuela.nombre}"