from django.contrib import admin

# Register your models here.
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('destinatario', 'titulo', 'leida', 'fecha_envio')
    list_filter = ('leida', 'fecha_envio')
    search_fields = ('titulo', 'mensaje', 'destinatario__username')