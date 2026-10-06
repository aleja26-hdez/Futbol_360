from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Entrenador
from .serializers import EntrenadorSerializer

class EntrenadorViewSet(viewsets.ModelViewSet):
    queryset = Entrenador.objects.all()
    serializer_class = EntrenadorSerializer