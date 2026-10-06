from django.contrib import admin

# Register your models here.
from .models import Jugador

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'edad', 'categoria', 'telefono_acudiente', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre_completo', 'direccion')