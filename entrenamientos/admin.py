from django.contrib import admin

# Register your models here.
from .models import Entrenamiento

@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'entrenador', 'fecha', 'hora_inicio', 'hora_fin', 'lugar')
    list_filter = ('categoria', 'entrenador', 'fecha')
    search_fields = ('tema', 'lugar')