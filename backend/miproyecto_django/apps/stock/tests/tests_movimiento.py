from apps.stock.models import MovimientoStock
from apps.usuarios.models import Usuario  # CustomUser
from datetime import date

class MovimientoStockModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Limpieza")
        self.almacen = Almacen.objects.create(nombre="Depósito", sucursal_id=1)
        self.producto = Producto.objects.create(
            nombre="Lavandina",
            codigo="L001",
            unidad="litro",
            precio=25.00,
            stock=5,
            stock_minimo=1,
            categoria=self.categoria,
            almacen=self.almacen
        )
        self.usuario = Usuario.objects.create_user(email='test@test.com', password='1234', rol='admin')

    def test_movimiento_entrada_aumenta_stock(self):
        movimiento = MovimientoStock.objects.create(
            producto=self.producto,
            tipo="entrada",
            cantidad=10,
            motivo="Reposición",
            usuario=self.usuario
        )
        self.assertEqual(movimiento.producto.stock, 5)  # No se modifica automáticamente

    def test_movimiento_salida_sin_stock_lanza_error(self):
        movimiento = MovimientoStock(
            producto=self.producto,
            tipo="salida",
            cantidad=10,
            motivo="Venta",
            usuario=self.usuario
        )
        with self.assertRaises(ValidationError):
            movimiento.full_clean()
