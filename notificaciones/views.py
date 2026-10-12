from rest_framework import viewsets
from usuarios.permissions import PadreSoloLectura
from .models import Notificacion
from .serializers import NotificacionSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Notificacion.objects.all()
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            qs = qs.filter(destinatario=user)
        return qs