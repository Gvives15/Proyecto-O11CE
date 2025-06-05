# apps/caja/serializers.py

from rest_framework import serializers
from .models import Caja, MovimientoCaja

class MovimientoCajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = ['id', 'fecha', 'tipo', 'monto', 'descripcion']

class CajaSerializer(serializers.ModelSerializer):
    movimientos = MovimientoCajaSerializer(many=True, read_only=True)

    class Meta:
        model = Caja
        fields = ['id', 'usuario', 'fecha_apertura', 'fecha_cierre', 'monto_inicial', 'monto_final', 'abierta', 'movimientos']
