from django.db import models

# Create your models here.
from usuarios.models import Usuario

class Notificacion(models.Model):
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Leída" if self.leida else "No leída"
        return f"{self.destinatario.username} - {self.titulo} ({estado})"

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_envio']

class DispositivoPush(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='dispositivos')
    token = models.CharField(max_length=255, unique=True)
    plataforma = models.CharField(max_length=20, default='android')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.plataforma}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"