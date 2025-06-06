from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from .models import Venta
from .serializers import VentaSerializer
from .filters import VentaFilter
from apps.caja.models import Caja, MovimientoCaja

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = VentaFilter

    
    def perform_create(self, serializer):
        usuario = self.request.user
        caja_abierta = Caja.objects.filter(usuario=usuario, abierta=True).last()
        if not caja_abierta:
            raise ValidationError("No hay caja abierta para registrar la venta.")
        venta = serializer.save(usuario=usuario, caja=caja_abierta)
        # Aquí podés crear el movimiento de caja automáticamente
        MovimientoCaja.objects.create(
            caja=caja_abierta,
            tipo='ingreso',
            monto=venta.total,
            descripcion=f'Venta #{venta.id}',
            usuario=usuario
        )
