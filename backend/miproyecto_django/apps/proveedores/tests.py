from django.test import TestCase
from apps.empresa.models import Empresa, Sucursal, Almacen
from apps.stock.models import Categoria, Subcategoria, Producto
from .models import Proveedor, Compra, DetalleCompra


class ProveedorModelTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(nombre="E", cuit="1", direccion="d", contacto="c")
        self.sucursal = Sucursal.objects.create(nombre="S", empresa=self.empresa, direccion="d")
        self.almacen = Almacen.objects.create(nombre="A", sucursal=self.sucursal)
        self.categoria = Categoria.objects.create(nombre="cat")
        self.subcategoria = Subcategoria.objects.create(nombre="sub", categoria=self.categoria)
        self.producto = Producto.objects.create(
            nombre="prod", codigo="P1", categoria=self.categoria,
            subcategoria=self.subcategoria, almacen=self.almacen,
            precio=10, stock=0, stock_minimo=1
        )
        self.proveedor = Proveedor.objects.create(nombre="Prov", cuit="20")
        self.compra = Compra.objects.create(proveedor=self.proveedor, almacen=self.almacen)

    def test_detalle_compra_subtotal(self):
        detalle = DetalleCompra.objects.create(
            compra=self.compra, producto=self.producto,
            cantidad=2, precio_unitario=5
        )
        self.assertEqual(detalle.subtotal(), 10)
        self.assertIn("Prov", str(self.proveedor))
