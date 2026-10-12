from rest_framework import serializers
from .models import Entrenador


class EntrenadorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()
    categorias_nombres = serializers.SerializerMethodField()

    class Meta:
        model = Entrenador
        fields = '__all__'

    def get_categorias_nombres(self, obj):
        return [c.nombre for c in obj.categorias.all()]