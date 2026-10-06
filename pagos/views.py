from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import EstadoPago, Abono
from .serializers import EstadoPagoSerializer, AbonoSerializer

class EstadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer

class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer