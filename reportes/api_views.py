from rest_framework.decorators import api_view
from rest_framework.response import Response

from asistencia.models import Asistencia
from entrenadores.models import Entrenador
from entrenamientos.models import Entrenamiento
from escuelas.models import Escuela
from jugadores.models import Jugador
from notificaciones.models import Notificacion
from pagos.models import EstadoPago
from usuarios.models import Usuario
from notificaciones.models import DispositivoPush

NO_AUTORIZADO = {'detail': 'No tienes permiso para esta acción'}


def _escuela_dict(e, request):
    return {
        'id': e.id,
        'nombre': e.nombre,
        'ciudad': e.ciudad,
        'direccion': e.direccion,
        'edad_minima': e.edad_minima,
        'edad_maxima': e.edad_maxima,
        'telefono': e.telefono,
        'instagram': e.instagram,
        'facebook': e.facebook,
        'fecha_registro': e.fecha_registro,
        'logo': request.build_absolute_uri(e.logo.url) if e.logo else None,
        'fotos': [
            {
                'id': f.id,
                'descripcion': f.descripcion,
                'imagen': request.build_absolute_uri(f.imagen.url),
            }
            for f in e.fotos.all()
        ],
    }


@api_view(['GET'])
def dashboard(request):
    if request.user.rol != 'directivo':
        return Response(NO_AUTORIZADO, status=403)
    return Response({
        'total_jugadores': Jugador.objects.filter(activo=True).count(),
        'pendientes': EstadoPago.objects.filter(estado='pendiente').count(),
        'abonados': EstadoPago.objects.filter(estado='abonado').count(),
        'cancelados': EstadoPago.objects.filter(estado='cancelado').count(),
    })


@api_view(['GET'])
def escuela(request):
    e = request.user.escuela or Escuela.objects.first()
    return Response(_escuela_dict(e, request) if e else None)


@api_view(['GET'])
def escuelas(request):
    if request.user.rol != 'directivo':
        return Response(NO_AUTORIZADO, status=403)
    return Response([_escuela_dict(e, request) for e in Escuela.objects.all()])


@api_view(['GET', 'POST'])
def planilla(request, entrenamiento_id):
    """Pasar asistencia: solo el entrenador dueño del entrenamiento."""
    if request.user.rol != 'entrenador':
        return Response(NO_AUTORIZADO, status=403)
    entrenamiento = Entrenamiento.objects.filter(
        id=entrenamiento_id, entrenador__usuario=request.user
    ).first()
    if not entrenamiento:
        return Response(NO_AUTORIZADO, status=403)

    jugadores = Jugador.objects.filter(categoria=entrenamiento.categoria)

    if request.method == 'POST':
        presentes = set(request.data.get('presentes', []))
        for j in jugadores:
            Asistencia.objects.update_or_create(
                entrenamiento=entrenamiento,
                jugador=j,
                defaults={'presente': j.id in presentes},
            )
        return Response({'ok': True})

    marcados = dict(
        Asistencia.objects.filter(entrenamiento=entrenamiento)
        .values_list('jugador_id', 'presente')
    )
    return Response({
        'entrenamiento': str(entrenamiento),
        'jugadores': [
            {'id': j.id, 'nombre': j.nombre_completo, 'presente': marcados.get(j.id, False)}
            for j in jugadores
        ],
    })


def _padres_permitidos(user):
    if user.rol == 'directivo':
        return Usuario.objects.filter(rol='padre')
    entrenador = Entrenador.objects.filter(usuario=user).first()
    if not entrenador:
        return Usuario.objects.none()
    jugadores = Jugador.objects.filter(categoria__in=entrenador.categorias.all())
    return Usuario.objects.filter(id__in=jugadores.values_list('acudiente', flat=True))


@api_view(['GET'])
def notificaciones_enviadas(request):
    if request.user.rol == 'directivo':
        qs = Notificacion.objects.all()
    elif request.user.rol == 'entrenador':
        qs = Notificacion.objects.filter(destinatario__in=_padres_permitidos(request.user))
    else:
        return Response(NO_AUTORIZADO, status=403)
    return Response([
        {
            'id': n.id,
            'destinatario_nombre': n.destinatario.get_full_name() or n.destinatario.username,
            'titulo': n.titulo,
            'mensaje': n.mensaje,
            'leida': n.leida,
            'fecha_envio': n.fecha_envio,
        }
        for n in qs.select_related('destinatario')
    ])


@api_view(['GET'])
def destinatarios(request):
    if request.user.rol not in ('entrenador', 'directivo'):
        return Response(NO_AUTORIZADO, status=403)
    return Response([
        {'id': u.id, 'nombre': u.get_full_name() or u.username}
        for u in _padres_permitidos(request.user)
    ])


@api_view(['POST'])
def enviar_notificacion(request):
    if request.user.rol not in ('entrenador', 'directivo'):
        return Response(NO_AUTORIZADO, status=403)
    destinatario = _padres_permitidos(request.user).filter(
        id=request.data.get('destinatario')
    ).first()
    titulo = (request.data.get('titulo') or '').strip()
    mensaje = (request.data.get('mensaje') or '').strip()
    if not destinatario or not titulo or not mensaje:
        return Response({'detail': 'Elige un destinatario y completa título y mensaje'}, status=400)
    Notificacion.objects.create(destinatario=destinatario, titulo=titulo[:100], mensaje=mensaje)
    return Response({'ok': True}, status=201)

@api_view(['POST', 'DELETE'])
def dispositivo(request):
    token = (request.data.get('token') or '').strip()
    if not token:
        return Response({'detail': 'Falta el token del dispositivo'}, status=400)
    if request.method == 'POST':
        DispositivoPush.objects.update_or_create(
            token=token,
            defaults={
                'usuario': request.user,
                'plataforma': request.data.get('plataforma', 'android'),
            },
        )
        return Response({'ok': True})
    DispositivoPush.objects.filter(token=token, usuario=request.user).delete()
    return Response({'ok': True})