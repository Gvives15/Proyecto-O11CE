from rest_framework import serializers
from .models import Venta, DetalleVenta
from apps.stock.models import Producto

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_nombre', 'usuario', 'usuario_email', 'fecha', 'tipo_documento', 'total', 'descuento', 'confirmado', 'detalles', 'caja']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            producto = detalle_data['producto']
            cantidad = detalle_data['cantidad']
            if producto.stock < cantidad:
                raise serializers.ValidationError(f"Stock insuficiente para {producto.nombre}.")
            # Descontar stock
            producto.stock -= cantidad
            producto.save()
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        return venta
