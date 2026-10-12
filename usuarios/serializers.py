from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    escuela_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'rol', 'rol_display', 'escuela', 'escuela_nombre', 'is_active']
        # password no se incluye a propósito

    def get_escuela_nombre(self, obj):
        return obj.escuela.nombre if obj.escuela else ''