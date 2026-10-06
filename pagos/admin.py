from django.contrib import admin

# Register your models here.
from .models import EstadoPago, Abono

class AbonoInline(admin.TabularInline):
    model = Abono
    extra = 1

@admin.register(EstadoPago)
class EstadoPagoAdmin(admin.ModelAdmin):
    list_display = ('jugador', 'mes', 'valor_total', 'valor_abonado', 'saldo_pendiente', 'estado')
    list_filter = ('estado', 'mes')
    inlines = [AbonoInline]

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        form.instance.actualizar_estado()   # aquí se recalcula el estado automáticamente