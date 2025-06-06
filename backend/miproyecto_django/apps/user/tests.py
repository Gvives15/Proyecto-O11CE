from django.test import TestCase
from django.contrib.auth.models import Permission, ContentType
from .models import Rol, Usuario


class UsuarioModelTests(TestCase):
    def test_get_all_permissions(self):
        ct = ContentType.objects.get_for_model(Usuario)
        perm = Permission.objects.create(codename="users.test_perm", name="Test", content_type=ct)
        rol = Rol.objects.create(nombre="Admin")
        rol.permisos.add(perm)
        usuario = Usuario.objects.create_user(email="a@b.com", username="u", password="pass", rol=rol)
        perms = usuario.get_all_permissions()
        self.assertIn(perm, perms)
