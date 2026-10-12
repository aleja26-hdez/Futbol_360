from rest_framework import permissions


class PadreSoloLectura(permissions.BasePermission):
    """Los padres solo pueden leer. Los demás roles tienen acceso normal."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, 'rol', None) == 'padre':
            return request.method in permissions.SAFE_METHODS
        return True