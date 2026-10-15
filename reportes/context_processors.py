def notificaciones_sin_leer(request):
    if request.user.is_authenticated and getattr(request.user, 'rol', '') == 'padre':
        return {'sin_leer': request.user.notificaciones.filter(leida=False).count()}
    return {}