from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrVendedor(BasePermission):
    """Permite modificar solo a usuarios con rol admin o vendedor."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        rol = getattr(getattr(request.user, 'rol', None), 'nombre', None)
        if rol in {'admin', 'vendedor'} or request.user.is_staff or request.user.is_superuser:
            return True
        return False
