from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    SubcategoriaViewSet,
    ProductoViewSet,
    MovimientoStockViewSet,
    CargaMasivaProductosView,          
    AplicarAjustePreciosView,
    exportar_productos_excel
)


router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'subcategorias', SubcategoriaViewSet, basename='subcategoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'movimientos', MovimientoStockViewSet, basename='movimientostock')

urlpatterns = [
    path('', include(router.urls)),
    path('carga-masiva/', CargaMasivaProductosView.as_view(), name='carga-masiva-productos'),
    path('exportar/', exportar_productos_excel, name='exportar_productos_excel'),
    path('actualizar-precios/', AplicarAjustePreciosView.as_view(), name='aplicar-ajuste-precios'),
]
