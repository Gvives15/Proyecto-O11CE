from django.db import models
from apps.user.models import Usuario

class Caja(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    abierta = models.BooleanField(default=True)

    def __str__(self):
        return f"Caja {self.id} ({'Abierta' if self.abierta else 'Cerrada'})"

class MovimientoCaja(models.Model):
    caja = models.ForeignKey(Caja, related_name='movimientos', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')])
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo.title()} de ${self.monto} ({self.descripcion})"
