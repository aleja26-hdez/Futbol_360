from django.urls import path
from . import api_views
from torneos import api_llave

urlpatterns = [
    path('dashboard/', api_views.dashboard),
    path('escuela/', api_views.escuela),
    path('escuelas/', api_views.escuelas),
    path('planilla/<int:entrenamiento_id>/', api_views.planilla),
    path('notificaciones/enviadas/', api_views.notificaciones_enviadas),
    path('notificaciones/destinatarios/', api_views.destinatarios),
    path('notificaciones/enviar/', api_views.enviar_notificacion),
    path('dispositivos/', api_views.dispositivo),
    path('torneos/<int:torneo_id>/llave/', api_llave.llave_torneo),
    path('torneos/', api_llave.lista_torneos),
    path('notificaciones/<int:notificacion_id>/leer/', api_views.notificacion_leer),
    path('notificaciones/leer-todas/', api_views.notificaciones_leer_todas),
]