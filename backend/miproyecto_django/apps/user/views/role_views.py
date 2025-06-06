"""
ViewSet para CRUD de roles.
"""

from rest_framework import viewsets
from rest_framework.response import Response

from ..permissions import IsAdminOrHasPermission
from ..serializers import (
    RolSerializer,
    RolDetailSerializer,
    RolPermisosUpdateSerializer,
)
from ..models import Rol


class RolViewSet(viewsets.ModelViewSet):
    """
    CRUD de roles y asignación de permisos.
    """

    queryset = Rol.objects.prefetch_related("permisos")
    serializer_class = RolSerializer
    permission_classes = [IsAdminOrHasPermission]

    permission_map = {
        "list": "users.view_role",
        "retrieve": "users.view_role",
        "create": "users.add_role",
        "update": "users.change_role",
        "partial_update": "users.change_role",
        "destroy": "users.delete_role",
        "set_permissions": "users.change_role",
    }

    def get_serializer_class(self):
        if self.action in {"retrieve", "update", "partial_update"}:
            return RolDetailSerializer
        return super().get_serializer_class()

    # Acción extra para asignar permisos
    def set_permissions(self, request, pk=None):
        role = self.get_object()
        serializer = RolPermisosUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role.permisos.set(serializer.validated_data["permisos"])
        return Response({"detail": "Permisos asignados."})
