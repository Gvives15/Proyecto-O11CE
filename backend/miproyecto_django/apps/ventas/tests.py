from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.clientes.models import Cliente
from apps.caja.models import Caja
from apps.empresa.models import Empresa, Sucursal, Almacen
from apps.stock.models import Categoria, Subcategoria, Producto
from .models import Venta, DetalleVenta


class VentaModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="u@test.com", password="pass")
        self.caja = Caja.objects.create(usuario=self.user, monto_inicial=0)
        self.empresa = Empresa.objects.create(nombre="E", cuit="1", direccion="d", contacto="c")
        self.sucursal = Sucursal.objects.create(nombre="S", empresa=self.empresa, direccion="d")
        self.almacen = Almacen.objects.create(nombre="A", sucursal=self.sucursal)
        self.categoria = Categoria.objects.create(nombre="cat")
        self.subcategoria = Subcategoria.objects.create(nombre="sub", categoria=self.categoria)
        self.producto = Producto.objects.create(
            nombre="prod", codigo="P1", categoria=self.categoria,
            subcategoria=self.subcategoria, almacen=self.almacen,
            precio=10, stock=10, stock_minimo=1
        )
        self.cliente = Cliente.objects.create(
            nombre="c", apellido="l", dni="1", telefono="1", email="c@c.com", direccion="d"
        )

    def test_venta_str(self):
        venta = Venta.objects.create(cliente=self.cliente, usuario=self.user, total=10, caja=self.caja)
        DetalleVenta.objects.create(venta=venta, producto=self.producto, cantidad=1, precio_unitario=10, subtotal=10)
        self.assertTrue(str(venta).startswith("Venta #"))
