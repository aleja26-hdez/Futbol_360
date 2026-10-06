from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Entrenamiento
from .serializers import EntrenamientoSerializer

class EntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = Entrenamiento.objects.all()
    serializer_class = EntrenamientoSerializer