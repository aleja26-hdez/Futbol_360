from django.contrib import admin

# Register your models here.
from .models import Torneo, Partido

class PartidoInline(admin.TabularInline):
    model = Partido
    extra = 1

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'fecha_inicio', 'fecha_fin')
    list_filter = ('categoria',)
    inlines = [PartidoInline]


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('torneo', 'rival', 'fecha', 'hora', 'goles_favor', 'goles_contra')
    list_filter = ('torneo',)