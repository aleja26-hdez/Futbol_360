from django.contrib import admin

# Register your models here.
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'escuela', 'edad_minima', 'edad_maxima')
    list_filter = ('escuela',)
    search_fields = ('nombre',)