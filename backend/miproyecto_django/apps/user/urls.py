from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    LoginView,
    RolViewSet,
    PermisoViewSet
)

# Crea las rutas automáticas para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'permisos', PermisoViewSet, basename='permisos')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
