import django_filters
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    codigo = django_filters.CharFilter(field_name='codigo', lookup_expr='icontains')
    categoria = django_filters.CharFilter(field_name='categoria__nombre', lookup_expr='icontains')
    subcategoria = django_filters.CharFilter(field_name='subcategoria__nombre', lookup_expr='icontains')
    almacen = django_filters.NumberFilter(field_name='almacen__id')
    vencimiento_desde = django_filters.DateFilter(field_name='vencimiento', lookup_expr='gte')
    vencimiento_hasta = django_filters.DateFilter(field_name='vencimiento', lookup_expr='lte')
    stock_bajo = django_filters.BooleanFilter(method='filtrar_stock_bajo')

    class Meta:
        model = Producto
        fields = []

    def filtrar_stock_bajo(self, queryset, name, value):
        if value:
            return queryset.filter(stock__lt=django_filters.F('stock_minimo'))
        return queryset
