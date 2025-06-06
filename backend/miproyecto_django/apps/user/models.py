# users/models.py
"""Modelos personalizados de usuario y rol para el sistema de autenticación.

Este archivo define:
1. Rol: contenedor liviano encima de los permisos de Django.
2. Usuario: extiende AbstractUser, usa el email como identificador
   y añade soporte para Rol + permisos extra.

Buenas prácticas aplicadas
--------------------------
* Se utiliza `email` como campo único para iniciar sesión.
* Se define `USERNAME_FIELD = 'email'` y se añade un índice único.
* No se tocan los permisos por defecto de Django; se complementan.
"""

from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class Rol(models.Model):
    """Representa un rol con un conjunto de permisos asociado."""
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    permisos = models.ManyToManyField(
        Permission,
        verbose_name=_('permisos'),
        blank=True,
        help_text=_('Permisos que heredan los usuarios con este rol.'),
    )

    class Meta:
        verbose_name = _('rol')
        verbose_name_plural = _('roles')
        default_permissions = ()  # Se definen manualmente abajo
        permissions = [
            ('view_rol', _('Ver lista de roles')),
            ('add_rol', _('Crear roles')),
            ('change_rol', _('Modificar roles')),
            ('delete_rol', _('Eliminar roles')),
        ]

    def __str__(self) -> str:
        return self.nombre


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado.

    Se usa el email como nombre de usuario y se añade:
    * rol        -> relación con Rol
    * permisos_adicionales -> permisos directos aparte del rol
    """
    email = models.EmailField(_('correo electrónico'), unique=True)
    rol = models.ForeignKey(
        Rol,
        verbose_name=_('rol'),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    permisos_adicionales = models.ManyToManyField(
        Permission,
        verbose_name=_('permisos adicionales'),
        blank=True,
        help_text=_('Permisos asignados directamente al usuario.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Para compatibilidad con createsuperuser

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    # --- Métodos utilitarios -------------------------------------------------

    def get_all_permissions(self) -> set[Permission]:
        """
        Devuelve el conjunto completo de permisos del usuario:
        * permisos heredados del rol
        * permisos asignados directamente
        """
        permisos = set()
        if self.rol:
            permisos.update(self.rol.permisos.all())
        permisos.update(self.permisos_adicionales.all())
        return permisos

