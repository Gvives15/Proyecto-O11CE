from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.stock.models import Producto, MovimientoStock, Categoria, Subcategoria
from apps.empresa.models import Almacen, Sucursal, Empresa
from django.contrib.auth import get_user_model

class StockTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            password='pass1234'
        )
        self.client.login(email='admin@test.com', password='pass1234')

        self.empresa = Empresa.objects.create(
            nombre="Mi Empresa",
            cuit="30-12345678-9",
            direccion="Calle Falsa 123",
            contacto="011-4444-5555"
        )
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal 1",
            empresa=self.empresa,
            direccion="Sucursal Falsa 321",
            ubicacion="Ciudad X"
        )
        self.almacen = Almacen.objects.create(
            nombre="Principal",
            sucursal=self.sucursal
        )
        self.categoria = Categoria.objects.create(nombre="Alimentos")
        self.subcategoria = Subcategoria.objects.create(nombre="Galletitas", categoria=self.categoria)
        self.prod = Producto.objects.create(
            nombre="Galletitas",
            codigo="GAL01",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            almacen=self.almacen,
            precio=100,
            stock=10,
            stock_minimo=1
        )

    def test_creacion_producto(self):
        count = Producto.objects.count()
        cat_bebidas = Categoria.objects.create(nombre="Bebidas")
        sub_bebidas = Subcategoria.objects.create(nombre="Agua", categoria=cat_bebidas)
        prod = Producto.objects.create(
            nombre="Agua",
            codigo="AGUA01",
            categoria=cat_bebidas,
            subcategoria=sub_bebidas,
            almacen=self.almacen,
            precio=50,
            stock=20,
            stock_minimo=1
        )
        self.assertEqual(Producto.objects.count(), count + 1)

    def test_edicion_producto(self):
        self.prod.nombre = "Galletitas Choco"
        self.prod.save()
        # El modelo guarda en minúsculas
        self.assertEqual(Producto.objects.get(id=self.prod.id).nombre, "galletitas choco")

    def test_eliminacion_producto(self):
        prod_id = self.prod.id
        self.prod.delete()
        self.assertFalse(Producto.objects.filter(id=prod_id).exists())

    def test_stock_negativo(self):
        self.prod.stock = -5
        with self.assertRaises(Exception):
            self.prod.save()

    def test_movimiento_stock_entrada(self):
        stock_inicial = self.prod.stock
        mov = MovimientoStock.objects.create(
            producto=self.prod,
            tipo='entrada',
            cantidad=5,
            usuario=self.user
        )
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, stock_inicial + 5)

    def test_movimiento_stock_salida(self):
        stock_inicial = self.prod.stock
        mov = MovimientoStock.objects.create(
            producto=self.prod,
            tipo='salida',
            cantidad=3,
            usuario=self.user
        )
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, stock_inicial - 3)

    def test_movimiento_stock_salida_mayor_stock(self):
        with self.assertRaises(Exception):
            MovimientoStock.objects.create(
                producto=self.prod,
                tipo='salida',
                cantidad=self.prod.stock + 1,
                usuario=self.user
            )

    def test_filtro_por_categoria(self):
        res = Producto.objects.filter(categoria=self.categoria)
        self.assertIn(self.prod, res)

    def test_importar_productos_por_excel(self):
        with open("tmp/productos_prueba_masiva.xlsx", "rb") as f:
            archivo = SimpleUploadedFile(
                "productos_prueba_masiva.xlsx",
                f.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        response = self.client.post(
            reverse('carga-masiva-productos'),
            {'file': archivo}  # <--- clave: 'file' según tu view
        )
        self.assertEqual(response.status_code, 200)

    def test_exportar_excel(self):
        response = self.client.get(reverse('exportar_productos_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            response['Content-Type']
        )

    def test_historial_movimientos(self):
        mov = MovimientoStock.objects.create(
            producto=self.prod,
            tipo='entrada',
            cantidad=2,
            usuario=self.user
        )
        historial = MovimientoStock.objects.filter(producto=self.prod)
        self.assertIn(mov, historial)

   def test_previsualizar_ajuste_precios(self):
        url = '/api/v1/stock/actualizar-precios-preview/'
        data = {
            'tipo': 'cat',
            'id': self.categoria.id,
            'porcentaje': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total_afectados'), 1)
        productos = response.json().get('productos')
        self.assertEqual(productos[0]['precio_nuevo'], 110.0)

    def test_aplicar_ajuste_precios(self):
        url = '/api/v1/stock/actualizar-precios/'
        data = {
            'tipo': 'cat',
            'id': self.categoria.id,
            'porcentaje': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.prod.refresh_from_db()
        self.assertEqual(float(self.prod.precio), 110.0)

    # def test_permisos_usuario(self):
    #     # PENDIENTE: Se implementa cuando el módulo de usuario/roles esté activo
    #     pass