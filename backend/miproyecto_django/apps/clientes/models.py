from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, default='Juan')
    apellido = models.CharField(max_length=100, default='Pérez')
    dni = models.CharField(max_length=10, unique=True, default='00000000')
    telefono = models.CharField(max_length=20, default='0000000000')
    email = models.EmailField(default='cliente@ejemplo.com')
    direccion = models.CharField(max_length=255, default='Sin dirección')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
