from rest_framework import serializers
from .models import Torneo, Partido


class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'


class TorneoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    partidos = PartidoSerializer(many=True, read_only=True)

    class Meta:
        model = Torneo
        fields = '__all__' 