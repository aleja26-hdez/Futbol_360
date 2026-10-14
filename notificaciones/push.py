import json
import logging

import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging

logger = logging.getLogger(__name__)


def _iniciar():
    try:
        firebase_admin.get_app()
        return True
    except ValueError:
        pass
    try:
        if settings.FIREBASE_CREDENTIALS_JSON:
            cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))
        elif settings.FIREBASE_CREDENTIALS_FILE.exists():
            cred = credentials.Certificate(str(settings.FIREBASE_CREDENTIALS_FILE))
        else:
            logger.warning('Firebase no está configurado: no se envían notificaciones push')
            return False
        firebase_admin.initialize_app(cred)
        return True
    except Exception:
        logger.exception('No se pudo iniciar Firebase')
        return False


def enviar_push(usuario, titulo, cuerpo, datos=None):
    """Envía un push a todos los celulares del usuario. Nunca rompe el flujo si falla."""
    try:
        tokens = list(usuario.dispositivos.values_list('token', flat=True))
        if not tokens or not _iniciar():
            return

        mensaje = messaging.MulticastMessage(
            tokens=tokens,
            notification=messaging.Notification(title=titulo, body=cuerpo),
            data={k: str(v) for k, v in (datos or {}).items()},
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(channel_id='avisos'),
            ),
        )
        respuesta = messaging.send_each_for_multicast(mensaje)

        # Borra los tokens que ya no sirven (app desinstalada, etc.)
        for token, r in zip(tokens, respuesta.responses):
            if not r.success and isinstance(r.exception, messaging.UnregisteredError):
                usuario.dispositivos.filter(token=token).delete()
    except Exception:
        logger.exception('Error enviando notificación push')