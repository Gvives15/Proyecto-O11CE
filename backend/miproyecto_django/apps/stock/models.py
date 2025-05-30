from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from apps.empresa.models import Almacen

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, default='General')
    descripcion = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100, default='Sin subcategoría')

    def __str__(self):
        return self.nombre


import unicodedata
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from apps.empresa.models import Almacen

def limpiar_texto(texto):
    if texto is None:
        return ''
    texto = texto.strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.lower()

class Producto(models.Model):
    nombre = models.CharField(max_length=255, default='Producto sin nombre')
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, default='')
    unidad = models.CharField(max_length=50, default='unidad')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vencimiento = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey('Subcategoria', on_delete=models.SET_NULL, null=True, blank=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)

    def get_stock_minimo(self):
        return self.stock_minimo if self.stock_minimo is not None else 10

    def clean(self):
        self.codigo = limpiar_texto(self.codigo)
        self.nombre = limpiar_texto(self.nombre)
        self.unidad = limpiar_texto(self.unidad)
        self.descripcion = self.descripcion.strip() if self.descripcion else ''

        if not self.codigo:
            raise ValidationError("El código no puede estar vacío.")
        if not self.nombre:
            raise ValidationError("El nombre no puede estar vacío.")
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0.")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.stock_minimo is None or self.stock_minimo < 1:
            raise ValidationError("El stock mínimo debe ser al menos 1.")
        if self.vencimiento and self.vencimiento < date.today():
            raise ValidationError("La fecha de vencimiento no puede estar en el pasado.")
        if not self.categoria:
            raise ValidationError("Debe tener una categoría.")
        if not self.almacen:
            raise ValidationError("Debe estar asignado a un almacén.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre.capitalize()} ({self.codigo.upper()})'

from django.db import models
from django.core.exceptions import ValidationError
#from apps.user.models import usuario
from apps.stock.models import Producto
from datetime import date

class MovimientoStock(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    TIPO_CHOICES = [(ENTRADA, 'Entrada'), (SALIDA, 'Salida')]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100, blank=True)
    #usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if not self.tipo in dict(self.TIPO_CHOICES):
            raise ValidationError("Tipo de movimiento inválido.")

        if not self.usuario:
            raise ValidationError("El movimiento debe tener un usuario asignado.")

        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")

        if not self.producto:
            raise ValidationError("Debe seleccionar un producto.")

        if self.tipo == self.SALIDA and self.producto.stock < self.cantidad:
            raise ValidationError("Stock insuficiente para realizar la salida.")

    def save(self, *args, **kwargs):
        self.full_clean()

        # Actualizar stock del producto
        if self.tipo == self.ENTRADA:
            self.producto.stock += self.cantidad
        elif self.tipo == self.SALIDA:
            self.producto.stock -= self.cantidad
        self.producto.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.producto.nombre} x{self.cantidad}"


class AlertaSistema(models.Model):
    TIPO_CHOICES = [
        ('STOCK_BAJO', 'Stock bajo'),
        ('STOCK_NEGATIVO', 'Stock negativo'),
        ('SIN_CATEGORIA', 'Producto sin categoría'),
        ('VENCIMIENTO', 'Producto por vencer'),
    ]

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    referencia = models.CharField(max_length=255)  # nombre del producto afectado
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    procesada = models.BooleanField(default=False)  # Para saber si ya se notificó

    def __str__(self):
        return f"[{self.tipo}] {self.referencia}"
