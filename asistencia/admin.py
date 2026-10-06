from django.contrib import admin

# Register your models here.
from .models import Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('jugador', 'entrenamiento', 'presente', 'fecha_registro')
    list_filter = ('presente', 'entrenamiento__categoria', 'entrenamiento__fecha')
    search_fields = ('jugador__nombre_completo',)