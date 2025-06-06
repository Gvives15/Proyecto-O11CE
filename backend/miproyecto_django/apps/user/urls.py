"""
Enrutado de la app users.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user.views.auth_views import RegisterView, LoginView, LogoutView
from apps.user.views.user_views import UserViewSet
from apps.user.views.role_views import RoleViewSet
from apps.user.views.permissions_views import PermissionListView

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuario")
router.register(r"roles", RoleViewSet, basename="role")

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
