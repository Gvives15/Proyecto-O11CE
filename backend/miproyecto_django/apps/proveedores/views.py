from rest_framework import viewsets
from .models import Proveedor, Compra
from .serializers import ProveedorSerializer, CompraSerializer
from rest_framework.permissions import IsAuthenticated

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all().order_by('-fecha')
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]
