# Proyecto O11CE - Documentación

Este directorio contiene información general del backend desarrollado en Django.

## Estructura

El código fuente vive en `backend/miproyecto_django`. Allí se encuentran las diferentes apps de la plataforma:

- **user**: autenticación, roles y permisos.
- **clientes**: gestión de clientes.
- **proveedores**: proveedores y compras de mercadería.
- **stock**: productos y movimientos de inventario.
- **ventas**: registro de ventas.
- **caja**: apertura y cierre de cajas.
- **empresa**: datos de empresa, sucursales y almacenes.
- **core**: auditoría y utilidades comunes.

Cada app expone endpoints REST a través de `urls.py`.

## Ejecutar pruebas

Desde la carpeta `backend/miproyecto_django` ejecuta:

```bash
python manage.py test
```

Las pruebas utilizan la base de datos en memoria de Django, por lo que no
requieren configuración adicional.
