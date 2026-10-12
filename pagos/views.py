from rest_framework import viewsets
from usuarios.permissions import PadreSoloLectura
from .models import EstadoPago, Abono
from .serializers import EstadoPagoSerializer, AbonoSerializer


class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = EstadoPago.objects.select_related('jugador').prefetch_related('abonos')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            qs = qs.filter(jugador__acudiente=user)
        return qs


class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer
    permission_classes = [PadreSoloLectura]

    def get_queryset(self):
        qs = Abono.objects.select_related('estado_pago__jugador')
        user = self.request.user
        if getattr(user, 'rol', None) == 'padre':
            qs = qs.filter(estado_pago__jugador__acudiente=user)
        return qs