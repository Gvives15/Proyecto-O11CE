from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Caja, MovimientoCaja


class CajaModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="pass")

    def test_caja_str(self):
        caja = Caja.objects.create(usuario=self.user, monto_inicial=100)
        self.assertTrue(str(caja).startswith("Caja"))

    def test_movimiento_str_and_relation(self):
        caja = Caja.objects.create(usuario=self.user, monto_inicial=50)
        mov = MovimientoCaja.objects.create(
            caja=caja, tipo="ingreso", monto=10, descripcion="test"
        )
        self.assertIn("Ingreso", str(mov))
        self.assertEqual(caja.movimientos.count(), 1)
