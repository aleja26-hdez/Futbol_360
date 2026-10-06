from django.contrib import admin

# Register your models here.
from .models import Entrenador

@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'telefono', 'especialidad')
    filter_horizontal = ('categorias',)