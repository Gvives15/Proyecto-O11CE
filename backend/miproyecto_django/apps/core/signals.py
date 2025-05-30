from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

def datos_a_dict(instance):
    return {f.name: getattr(instance, f.name) for f in instance._meta.fields if f.name != 'password'}

def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    from apps.core.models import Auditoria
    Auditoria.objects.create(
        accion='creado' if created else 'modificado',
        modelo=sender.__name__,
        instancia_id=instance.id,
        usuario=getattr(instance, '_usuario', None),
        datos_nuevos=str(datos_a_dict(instance))
    )

def registrar_auditoria_eliminado(sender, instance, **kwargs):
    from apps.core.models import Auditoria
    Auditoria.objects.create(
        accion='eliminado',
        modelo=sender.__name__,
        instancia_id=instance.id,
        usuario=getattr(instance, '_usuario', None),
        datos_previos=str(datos_a_dict(instance))
    )
