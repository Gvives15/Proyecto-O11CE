from django.test import TestCase
from apps.stock.models import Producto, Categoria
from apps.empresa.models import Almacen
from django.core.exceptions import ValidationError

class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Bebidas")
        self.almacen = Almacen.objects.create(nombre="Central", sucursal_id=1)

    def test_producto_stock_minimo_por_defecto(self):
        producto = Producto.objects.create(
            nombre="Agua",
            codigo="001",
            unidad="unidad",
            precio=10.00,
            stock=50,
            categoria=self.categoria,
            almacen=self.almacen
        )
        self.assertEqual(producto.get_stock_minimo(), 10)

    def test_producto_con_stock_negativo_lanza_error(self):
        producto = Producto(
            nombre="Agua",
            codigo="002",
            unidad="unidad",
            precio=10.00,
            stock=-5,
            stock_minimo=3,
            categoria=self.categoria,
            almacen=self.almacen
        )
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_producto_con_stock_minimo_none_lanza_error(self):
        producto = Producto(
            nombre="Agua",
            codigo="003",
            unidad="unidad",
            precio=10.00,
            stock=10,
            stock_minimo=None,
            categoria=self.categoria,
            almacen=self.almacen
        )
        with self.assertRaises(ValidationError):
            producto.full_clean()
