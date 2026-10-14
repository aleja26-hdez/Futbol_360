from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notificacion
from .push import enviar_push


@receiver(post_save, sender=Notificacion)
def notificar_por_push(sender, instance, created, **kwargs):
    if not created:
        return
    # Texto genérico a propósito: es lo que se ve en la pantalla bloqueada.
    # El detalle se lee dentro de la app, con la sesión iniciada.
    transaction.on_commit(lambda: enviar_push(
        instance.destinatario,
        'GolPro Manager',
        'Tienes un nuevo aviso de la escuela',
        {'tipo': 'notificacion', 'id': instance.id},
    ))