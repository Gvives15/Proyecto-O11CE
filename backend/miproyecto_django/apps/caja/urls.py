# apps/caja/urls.py

from rest_framework.routers import DefaultRouter
from .views import CajaViewSet, MovimientoCajaViewSet

router = DefaultRouter()
router.register(r'cajas', CajaViewSet, basename='cajas')
router.register(r'movimientos-caja', MovimientoCajaViewSet, basename='movimientos-caja')

urlpatterns = router.urls
