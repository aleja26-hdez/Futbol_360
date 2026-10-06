from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Escuela, FotoInstalacion

class FotoInstalacionInline(admin.TabularInline):
    model = FotoInstalacion
    extra = 1   # cuántos espacios vacíos para agregar fotos nuevas aparecen por defecto

@admin.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'telefono')
    search_fields = ('nombre', 'ciudad')
    inlines = [FotoInstalacionInline]