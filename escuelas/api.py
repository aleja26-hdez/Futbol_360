from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Escuela, FotoInstalacion


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoInstalacion
        fields = ['id', 'imagen', 'descripcion']


class EscuelaSerializer(serializers.ModelSerializer):
    fotos = FotoSerializer(many=True, read_only=True)

    class Meta:
        model = Escuela
        fields = ['id', 'nombre', 'ciudad', 'direccion', 'edad_minima', 'edad_maxima',
                  'telefono', 'instagram', 'facebook', 'logo', 'fotos']


class EscuelaInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        escuela = getattr(request.user, 'escuela', None) or Escuela.objects.first()
        if not escuela:
            return Response({})
        return Response(EscuelaSerializer(escuela, context={'request': request}).data)