from rest_framework import viewsets
from jugadores.models import Jugador
from usuarios.permissions import PadreSoloLectura
from .models import Entrenamiento
from .serializers import EntrenamientoSerializer


class EntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = Entrenamiento.objects.all()
    serializer_class = EntrenamientoSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Entrenamiento.objects.select_related('categoria', 'entrenador')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            categorias = Jugador.objects.filter(acudiente=user).values_list('categoria', flat=True)
            qs = qs.filter(categoria__in=categorias)
        return qs