from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Auditoria(models.Model):
    ACCIONES = (
        ('creado', 'Creado'),
        ('modificado', 'Modificado'),
        ('eliminado', 'Eliminado'),
    )

    accion = models.CharField(max_length=50, choices=ACCIONES)
    modelo = models.CharField(max_length=100)
    instancia_id = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(default=now)
    datos_previos = models.TextField(blank=True, null=True)
    datos_nuevos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha:%Y-%m-%d %H:%M} | {self.modelo} #{self.instancia_id} | {self.accion.upper()}"
