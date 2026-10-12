from rest_framework import serializers
from .models import Asistencia


class AsistenciaSerializer(serializers.ModelSerializer):
    jugador_nombre = serializers.CharField(source='jugador.nombre_completo', read_only=True)
    entrenamiento_texto = serializers.SerializerMethodField()

    class Meta:
        model = Asistencia
        fields = '__all__'

    def get_entrenamiento_texto(self, obj):
        return str(obj.entrenamiento)