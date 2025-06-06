"""
ViewSet para CRUD de usuarios.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from users.permissions import IsAdminOrHasPermission
from users.serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserPermissionUpdateSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuarios.
    """

    queryset = User.objects.select_related("rol").prefetch_related("permisos_adicionales")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrHasPermission]

    # Mapeo acción → permiso requerido
    permission_map = {
        "list": "users.view_usuario",
        "retrieve": "users.view_usuario",
        "create": "users.add_usuario",
        "update": "users.change_usuario",
        "partial_update": "users.change_usuario",
        "destroy": "users.delete_usuario",
        "set_extra_permissions": "users.change_usuario",
    }

    def get_serializer_class(self):
        if self.action in {"retrieve", "update", "partial_update"}:
            return UserDetailSerializer
        return super().get_serializer_class()

    # Acción extra para actualizar permisos adicionales
    def set_extra_permissions(self, request, pk=None):
        user = self.get_object()
        serializer = UserPermissionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.permisos_adicionales.set(serializer.validated_data["permisos"])
        return Response({"detail": "Permisos actualizados."})
