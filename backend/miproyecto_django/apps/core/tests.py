from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Auditoria


class AuditoriaModelTests(TestCase):
    def test_str(self):
        user = get_user_model().objects.create_user(email="u@test.com", password="pass")
        audit = Auditoria.objects.create(modelo="Test", instancia_id=1, accion="creado", usuario=user)
        self.assertIn("Test", str(audit))
