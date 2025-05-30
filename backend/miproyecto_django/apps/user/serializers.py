from rest_framework import serializers
from .models import CustomUser, Rol, Permiso


# 🔹 1. Serializador de Permisos (lectura)
# Este muestra los permisos completos: id, nombre, código y descripción
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['id', 'nombre', 'codigo', 'descripcion']


# 🔹 2. Serializador de Roles (lectura)
# Muestra el nombre del rol, su descripción y todos los permisos asociados
class RolSerializer(serializers.ModelSerializer):
    permisos = PermisoSerializer(many=True, read_only=True)

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'permisos']


# 🔹 3. Serializador de Usuario (lectura)
# Muestra todos los datos importantes del usuario y los permisos extra que tiene
class CustomUserSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    permisos_extra = PermisoSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'rol', 'permisos_extra', 'is_active', 'created_at'
        ]
class CustomUserCreateUpdateSerializer(serializers.ModelSerializer):
    # Esta línea permite que permisos_extra se pase como una lista de IDs (por ej: [1, 3, 7])
    permisos_extra = serializers.PrimaryKeyRelatedField(
        queryset=Permiso.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'rol', 'sucursal',
            'permisos_extra', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # no se devuelve al cliente
        }

    def create(self, validated_data):
        permisos = validated_data.pop('permisos_extra', [])
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        user.permisos_extra.set(permisos)
        return user

    def update(self, instance, validated_data):
        permisos = validated_data.pop('permisos_extra', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value) 
        if password:
            instance.set_password(password)
        instance.save()
        if permisos is not None:
            instance.permisos_extra.set(permisos)
        return instance
