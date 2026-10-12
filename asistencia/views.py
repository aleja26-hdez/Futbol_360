from rest_framework import viewsets
from usuarios.permissions import PadreSoloLectura
from .models import Asistencia
from .serializers import AsistenciaSerializer


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Asistencia.objects.select_related('entrenamiento__categoria', 'jugador')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            qs = qs.filter(jugador__acudiente=user)
        return qs