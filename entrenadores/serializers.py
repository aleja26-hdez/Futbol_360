from rest_framework import serializers
from .models import Entrenador

class EntrenadorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Entrenador
        fields = '__all__'