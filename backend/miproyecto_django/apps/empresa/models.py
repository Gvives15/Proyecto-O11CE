from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, default='Empresa Ejemplo')
    cuit = models.CharField(max_length=13, unique=True, default='00000000000')
    direccion = models.CharField(max_length=255, default='Sin dirección')
    contacto = models.CharField(max_length=100, default='contacto@empresa.com')

    def __str__(self):
        return f"{self.nombre} - {self.cuit}"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Sucursal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=100, default='Sucursal Central')
    direccion = models.CharField(max_length=255, default='Sin dirección')
    ubicacion = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"

    class Meta:
        ordering = ['empresa__nombre', 'nombre']
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'


class Almacen(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='almacenes')
    nombre = models.CharField(max_length=100, default='Almacén Principal')
    descripcion = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.nombre} - {self.sucursal.nombre}"

    class Meta:
        ordering = ['sucursal__nombre', 'nombre']
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'
