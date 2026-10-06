from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from escuelas.models import Escuela

class Usuario(AbstractUser):
    ROLES = [
        ('directivo', 'Directivo'),
        ('entrenador', 'Entrenador'),
        ('padre', 'Padre de familia'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['rol']