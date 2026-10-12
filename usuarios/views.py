from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        return Response(self.get_serializer(request.user).data)