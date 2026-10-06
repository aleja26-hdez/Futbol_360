from rest_framework import serializers
from .models import Torneo, Partido

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

class TorneoSerializer(serializers.ModelSerializer):
    partidos = PartidoSerializer(many=True, read_only=True)

    class Meta:
        model = Torneo
        fields = '__all__'