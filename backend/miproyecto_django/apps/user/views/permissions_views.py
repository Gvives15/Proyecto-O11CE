"""
Vista de solo lectura para listar todos los permisos disponibles.
"""

from django.contrib.auth.models import Permission
from rest_framework import generics

from apps.user.serializers import PermissionSerializer
from apps.user.permissions import IsAdminOrHasPermission


class PermissionListView(generics.ListAPIView):
    """
    Devuelve todos los permisos del sistema.
    """
    queryset = Permission.objects.all().select_related("content_type")
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminOrHasPermission]
    # Acceso sólo a quien tenga users.view_permission
    permission_map = {"list": "users.view_permission"}
