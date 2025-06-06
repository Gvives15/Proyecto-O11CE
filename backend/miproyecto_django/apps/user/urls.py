"""
Enrutado de la app users.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.auth_views import RegisterView, LoginView, LogoutView
from .views.user_views import UserViewSet
from .views.role_views import RolViewSet
from .views.permissions_views import PermissionListView

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuario")
router.register(r"roles", RolViewSet, basename="role")

urlpatterns = [
    # Endpoints de autenticación
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    # Permisos globales
    path("permisos/", PermissionListView.as_view(), name="permission-list"),
    # CRUD de usuarios y roles
    path("", include(router.urls)),
]
