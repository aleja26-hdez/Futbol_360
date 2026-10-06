from rest_framework import serializers
from .models import Jugador

class JugadorSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()

    class Meta:
        model = Jugador
        fields = '__all__'