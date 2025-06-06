from django.test import TestCase
from .models import Empresa, Sucursal, Almacen


class EmpresaModelTests(TestCase):
    def test_str_methods(self):
        empresa = Empresa.objects.create(nombre="Emp", cuit="1", direccion="d", contacto="c")
        sucursal = Sucursal.objects.create(nombre="Suc", empresa=empresa, direccion="d")
        almacen = Almacen.objects.create(nombre="Alm", sucursal=sucursal)
        self.assertEqual(str(empresa), "Emp - 1")
        self.assertIn("Emp", str(sucursal))
        self.assertIn("Suc", str(almacen))
