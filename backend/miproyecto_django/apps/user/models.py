from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from apps.empresa.models import Sucursal

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, default='Sin nombre')
    codigo = models.CharField(max_length=100, unique=True, default='sin_codigo')
    descripcion = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True, default='sin_rol')
    descripcion = models.TextField(blank=True, default='')
    permisos = models.ManyToManyField(Permiso, blank=True)

    def __str__(self):
        return self.nombre 


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    permisos_extra = models.ManyToManyField(Permiso, blank=True, related_name='usuarios_con_permiso_extra')
    sucursal = models.ForeignKey("empresa.Sucursal", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_permisos_completos(self):
        """Devuelve todos los permisos del usuario (rol + extras)."""
        permisos_rol = set(self.rol.permisos.all()) if self.rol else set()
        permisos_extras = set(self.permisos_extra.all())
        return permisos_rol.union(permisos_extras)

