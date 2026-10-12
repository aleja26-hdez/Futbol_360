from rest_framework import serializers
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    escuela_nombre = serializers.CharField(source='escuela.nombre', read_only=True)

    class Meta:
        model = Categoria
        fields = '__all__'