from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.clientes.models import Cliente
from django.contrib.auth import get_user_model
from apps.user.models import Rol

User = get_user_model()


class ClienteAPITestCase(APITestCase):
    def setUp(self):
        admin_role = Rol.objects.create(nombre='admin')
        vendedor_role = Rol.objects.create(nombre='vendedor')
        viewer_role = Rol.objects.create(nombre='viewer')

        self.admin_user = User.objects.create_user(
            email='admin@example.com', first_name='Admin', last_name='User',
            password='adminpass', rol=admin_role
        )
        self.vendedor_user = User.objects.create_user(
            email='vendor@example.com', first_name='Vendor', last_name='User',
            password='vendorpass', rol=vendedor_role
        )
        self.viewer_user = User.objects.create_user(
            email='viewer@example.com', first_name='Viewer', last_name='User',
            password='viewerpass', rol=viewer_role
        )

        self.list_url = '/api/v1/clientes/clientes/'

    def get_auth_header(self, user):
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token.access_token}'}

    def test_crear_cliente_valido(self):
        data = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'dni': '12345678',
            'telefono': '123456',
            'email': 'juan@example.com',
            'direccion': 'Calle 1',
            'saldo': '0.00'
        }
        response = self.client.post(self.list_url, data, **self.get_auth_header(self.admin_user))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_crear_cliente_dni_duplicado(self):
        Cliente.objects.create(nombre='a', apellido='b', dni='111', telefono='0', email='a@a.com', direccion='x')
        data = {
            'nombre': 'Otro',
            'apellido': 'Test',
            'dni': '111',
            'telefono': '123',
            'email': 'otro@example.com',
            'direccion': 'Calle 2'
        }
        response = self.client.post(self.list_url, data, **self.get_auth_header(self.admin_user))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_cliente_email_duplicado(self):
        Cliente.objects.create(nombre='a', apellido='b', dni='222', telefono='0', email='dup@example.com', direccion='x')
        data = {
            'nombre': 'Otro',
            'apellido': 'Test',
            'dni': '333',
            'telefono': '123',
            'email': 'dup@example.com',
            'direccion': 'Calle 2'
        }
        response = self.client.post(self.list_url, data, **self.get_auth_header(self.admin_user))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_clientes(self):
        Cliente.objects.create(nombre='a', apellido='b', dni='1', telefono='0', email='a@a.com', direccion='x')
        Cliente.objects.create(nombre='c', apellido='d', dni='2', telefono='0', email='c@c.com', direccion='y')
        response = self.client.get(self.list_url, **self.get_auth_header(self.viewer_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filtrar_por_nombre(self):
        Cliente.objects.create(nombre='Ana', apellido='b', dni='1', telefono='0', email='a@a.com', direccion='x')
        Cliente.objects.create(nombre='Beto', apellido='c', dni='2', telefono='0', email='b@b.com', direccion='y')
        response = self.client.get(f'{self.list_url}?search=Ana', **self.get_auth_header(self.viewer_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Ana')

    def test_actualizar_cliente(self):
        cliente = Cliente.objects.create(nombre='Ana', apellido='b', dni='99', telefono='0', email='ana@a.com', direccion='x')
        data = {'nombre': 'Ana Maria'}
        url = f'{self.list_url}{cliente.id}/'
        response = self.client.patch(url, data, **self.get_auth_header(self.vendedor_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, 'Ana Maria')

    def test_eliminar_cliente(self):
        cliente = Cliente.objects.create(nombre='Ana', apellido='b', dni='88', telefono='0', email='del@a.com', direccion='x')
        url = f'{self.list_url}{cliente.id}/'
        response = self.client.delete(url, **self.get_auth_header(self.admin_user))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_permiso_usuario_no_autorizado(self):
        data = {
            'nombre': 'Sin', 'apellido': 'Permiso', 'dni': '777',
            'telefono': '0', 'email': 'sin@permiso.com', 'direccion': 'x'
        }
        response = self.client.post(self.list_url, data, **self.get_auth_header(self.viewer_user))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
