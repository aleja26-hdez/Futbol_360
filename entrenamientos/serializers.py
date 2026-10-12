from rest_framework import serializers
from .models import Entrenamiento


class EntrenamientoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    entrenador_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Entrenamiento
        fields = '__all__'

    def get_entrenador_nombre(self, obj):
        return obj.entrenador.nombre_completo if obj.entrenador else ''