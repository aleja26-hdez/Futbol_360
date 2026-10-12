from django.urls import path
from . import api_views

urlpatterns = [
    path('dashboard/', api_views.dashboard),
    path('escuela/', api_views.escuela),
    path('escuelas/', api_views.escuelas),
    path('planilla/<int:entrenamiento_id>/', api_views.planilla),
    path('notificaciones/enviadas/', api_views.notificaciones_enviadas),
    path('notificaciones/destinatarios/', api_views.destinatarios),
    path('notificaciones/enviar/', api_views.enviar_notificacion),
]