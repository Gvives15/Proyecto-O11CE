from django.db import models
from apps.clientes.models import Cliente
from apps.stock.models import Producto
from apps.user.models import CustomUser
from apps.caja.models import Caja

class Venta(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('ticket', 'Ticket'),
        ('factura', 'Factura'),
        ('remito', 'Remito'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default='ticket')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    confirmado = models.BooleanField(default=True)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, null=True, blank=True)  # integra con caja

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.date()}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
