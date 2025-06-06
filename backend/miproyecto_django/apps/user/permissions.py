"""
Permisos personalizados para DRF.

‐ IsAdminOrHasPermission:  
   • Permite la acción si el usuario es “Administrador” **o** tiene el permiso
     asociado a la acción (por ejemplo `users.add_user`).  
   • El permiso requerido se define en la vista a través del atributo
     `permission_map` (dict action → codename).
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

ADMIN_ROLE_NAME = "Administrador"


class IsAdminOrHasPermission(BasePermission):
    """
    Permite el acceso si:
    1. El usuario está autenticado **y**  
       a) su rol se llama “Administrador”, **o**  
       b) posee el permiso específico mapeado para la acción.
    """

    def has_permission(self, request, view) -> bool:
        # El usuario debe estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False

        # El admin total siempre pasa
        if getattr(request.user.rol, "nombre", None) == ADMIN_ROLE_NAME:
            return True

        # Mapear la acción al codename necesario
        # Si la vista no define permission_map devolvemos False por seguridad
        permission_map = getattr(view, "permission_map", {})
        required_perm = permission_map.get(view.action)

        # Acciones de solo lectura sin mapear ⇒ permitir si tiene permiso de “view”
        if required_perm is None and request.method in SAFE_METHODS:
            return True

        # Verificar si el usuario tiene el permiso en cuestión
        return request.user.has_perm(required_perm) if required_perm else False
