from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ("email", "username", "rol", "is_staff")
    list_filter = ("is_staff", "is_superuser", "rol")
    search_fields = ("email", "username")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Datos adicionales", {"fields": ("rol", "permisos_adicionales")}),
    )
