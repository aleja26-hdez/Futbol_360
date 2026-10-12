from rest_framework import viewsets
from jugadores.models import Jugador
from usuarios.permissions import PadreSoloLectura
from .models import Torneo, Partido
from .serializers import TorneoSerializer, PartidoSerializer


class TorneoViewSet(viewsets.ModelViewSet):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Torneo.objects.prefetch_related('partidos')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            categorias = Jugador.objects.filter(acudiente=user).values_list('categoria', flat=True)
            qs = qs.filter(categoria__in=categorias)
        return qs


class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Partido.objects.select_related('torneo')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            categorias = Jugador.objects.filter(acudiente=user).values_list('categoria', flat=True)
            qs = qs.filter(torneo__categoria__in=categorias)
        return qs