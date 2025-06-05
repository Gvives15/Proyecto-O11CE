# apps/caja/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Caja, MovimientoCaja
from .serializers import CajaSerializer, MovimientoCajaSerializer
from rest_framework.decorators import action
from django.utils import timezone

class CajaViewSet(viewsets.ModelViewSet):
    queryset = Caja.objects.all().order_by('-fecha_apertura')
    serializer_class = CajaSerializer

    def create(self, request, *args, **kwargs):
        usuario = request.data.get('usuario')
        if Caja.objects.filter(usuario=usuario, abierta=True).exists():
            return Response({"error": "Ya existe una caja abierta para este usuario."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        caja = self.get_object()
        if not caja.abierta:
            return Response({"error": "La caja ya está cerrada."}, status=status.HTTP_400_BAD_REQUEST)
        monto_final = request.data.get('monto_final')
        if monto_final is None:
            return Response({"error": "Debes enviar el monto_final para cerrar la caja."}, status=status.HTTP_400_BAD_REQUEST)
        caja.monto_final = monto_final
        caja.fecha_cierre = timezone.now()
        caja.abierta = False
        caja.save()
        return Response(CajaSerializer(caja).data)

class MovimientoCajaViewSet(viewsets.ModelViewSet):
    queryset = MovimientoCaja.objects.all().order_by('-fecha')
    serializer_class = MovimientoCajaSerializer

    def create(self, request, *args, **kwargs):
        caja_id = request.data.get('caja')
        tipo = request.data.get('tipo')
        monto = float(request.data.get('monto', 0))
        if monto <= 0:
            return Response({"error": "El monto debe ser mayor a cero."}, status=status.HTTP_400_BAD_REQUEST)
        caja = Caja.objects.get(id=caja_id)
        if not caja.abierta:
            return Response({"error": "No se pueden registrar movimientos en una caja cerrada."}, status=status.HTTP_400_BAD_REQUEST)
        # Validación opcional: no permitir egresos mayores al saldo disponible
        if tipo == 'egreso':
            total_ingresos = sum([m.monto for m in caja.movimientos.filter(tipo='ingreso')])
            total_egresos = sum([m.monto for m in caja.movimientos.filter(tipo='egreso')])
            saldo = caja.monto_inicial + total_ingresos - total_egresos
            if monto > saldo:
                return Response({"error": "No hay suficiente saldo para este egreso."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
