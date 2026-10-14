from rest_framework.decorators import api_view
from rest_framework.response import Response

from entrenadores.models import Entrenador
from jugadores.models import Jugador
from . import llave
from .models import Torneo

NO_AUTORIZADO = {'detail': 'No tienes permiso para esta acción'}


@api_view(['GET', 'POST'])
def llave_torneo(request, torneo_id):
    torneo = Torneo.objects.select_related('categoria').filter(id=torneo_id).first()
    if not torneo or not llave.puede_ver(request.user, torneo):
        return Response(NO_AUTORIZADO, status=403)
    editable = llave.puede_editar(request.user, torneo)

    if request.method == 'POST':
        if not editable:
            return Response(NO_AUTORIZADO, status=403)
        try:
            llave.guardar_cruces(torneo, request.data.get('cruces', []))
        except ValueError as e:
            return Response({'detail': str(e)}, status=400)

    data = llave.armar_llave(torneo)
    data['puede_editar'] = editable
    return Response(data)

@api_view(['GET'])
def lista_torneos(request):
    user = request.user
    rol = getattr(user, 'rol', None)
    if rol == 'directivo':
        qs = Torneo.objects.all()
    elif rol == 'entrenador':
        e = Entrenador.objects.filter(usuario=user).first()
        qs = Torneo.objects.filter(categoria__in=e.categorias.all()) if e else Torneo.objects.none()
    elif rol == 'padre':
        cats = Jugador.objects.filter(acudiente=user).values_list('categoria', flat=True)
        qs = Torneo.objects.filter(categoria__in=cats)
    else:
        return Response(NO_AUTORIZADO, status=403)
    return Response([
        {'id': t.id, 'nombre': t.nombre, 'categoria': t.categoria.nombre,
         'fecha_inicio': t.fecha_inicio, 'fecha_fin': t.fecha_fin}
        for t in qs.select_related('categoria')
    ])