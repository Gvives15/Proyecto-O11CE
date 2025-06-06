# users/serializers.py
"""
Serializadores DRF para la app de usuarios.

Contiene:
* Serializador de permisos
* Serializadores de roles (lista y detalle)
* Serializadores de usuarios (lista, detalle, registro)
* Serializadores de actualización de permisos (rol y usuario)
"""

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Permission
from rest_framework import serializers

from .models import Rol, Usuario


# -------------------------- Permisos ---------------------------------------


class PermissionSerializer(serializers.ModelSerializer):
    """Serializa un permiso de Django."""
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name', 'content_type']


# -------------------------- Roles ------------------------------------------


class RolSerializer(serializers.ModelSerializer):
    """Serializador básico de rol (solo lectura de permisos)."""
    permisos = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'permisos']


class RolDetailSerializer(serializers.ModelSerializer):
    """Serializador de detalle de rol (permite actualizar permisos)."""
    permisos = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'permisos']


# -------------------------- Usuarios ---------------------------------------


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador de lista de usuarios."""
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'is_active', 'is_staff']


class UsuarioDetailSerializer(serializers.ModelSerializer):
    """Serializador de detalle de usuario (con permisos y rol)."""
    rol = RolDetailSerializer()
    permisos_adicionales = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'rol',
            'permisos_adicionales',
            'is_active',
            'is_staff',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializador para registrar un nuevo usuario.

    Valida la contraseña con las validaciones de Django
    (`AUTH_PASSWORD_VALIDATORS`).
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password', 'rol']

    # --------------- Validaciones -----------------

    def validate_password(self, value: str) -> str:
        """Valida la contraseña usando los validadores del proyecto."""
        validate_password(value)
        return value

    # --------------- Creación ---------------------

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


# ------- Serializadores de actualización de permisos -----------------------


class RolPermisosUpdateSerializer(serializers.Serializer):
    """Actualiza los permisos de un rol."""
    permisos = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    def update(self, instance: Rol, validated_data):
        instance.permisos.set(validated_data['permisos'])
        instance.save()
        return instance

    def create(self, validated_data):
        raise NotImplementedError('Solo se usa para actualizar.')


class UsuarioPermisosUpdateSerializer(serializers.Serializer):
    """Actualiza los permisos adicionales de un usuario."""
    permisos = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    def update(self, instance: Usuario, validated_data):
        instance.permisos_adicionales.set(validated_data['permisos'])
        instance.save()
        return instance

    def create(self, validated_data):
        raise NotImplementedError('Solo se usa para actualizar.')
