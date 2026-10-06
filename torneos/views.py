from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Torneo, Partido
from .serializers import TorneoSerializer, PartidoSerializer

class TorneoViewSet(viewsets.ModelViewSet):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer