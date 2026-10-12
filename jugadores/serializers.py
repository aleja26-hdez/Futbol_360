from rest_framework import serializers
from .models import Jugador


class JugadorSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    acudiente_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Jugador
        fields = '__all__'

    def get_acudiente_nombre(self, obj):
        if not obj.acudiente:
            return ''
        return obj.acudiente.get_full_name() or obj.acudiente.username