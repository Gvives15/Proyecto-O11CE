# apps/ventas/filters.py

import django_filters
from .models import Venta

class VentaFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateFilter(field_name="fecha", lookup_expr="gte")
    fecha_hasta = django_filters.DateFilter(field_name="fecha", lookup_expr="lte")
    cliente = django_filters.CharFilter(field_name="cliente__nombre", lookup_expr="icontains")
    tipo_documento = django_filters.CharFilter(field_name="tipo_documento", lookup_expr="iexact")
    usuario = django_filters.CharFilter(field_name="usuario__email", lookup_expr="icontains")

    class Meta:
        model = Venta
        fields = ["fecha_desde", "fecha_hasta", "cliente", "tipo_documento", "usuario"]
