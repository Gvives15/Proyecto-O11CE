# Proyecto O11CE

Este repositorio contiene el backend de **O11CE**, una aplicación Django que gestiona información de la empresa como clientes, proveedores, stock y ventas.

## Instalación

### Usando Docker

1. Ve a `backend/miproyecto_django`.
2. Crea un archivo `.env` con las variables de entorno indicadas abajo.
3. Construye e inicia los contenedores:
   ```bash
   docker-compose up --build
   ```
4. La aplicación estará disponible en `http://localhost:8001`.

### Entorno local

1. Crea y activa un entorno virtual de Python.
2. Instala las dependencias:
   ```bash
   pip install -r backend/miproyecto_django/requirements.txt
   ```
3. Define las variables de entorno que se listan más abajo.
4. Ejecuta las migraciones e inicia el servidor de desarrollo:
   ```bash
   cd backend/miproyecto_django
   python manage.py migrate
   python manage.py runserver
   ```

## Ejecutar tests

Para ejecutar las pruebas dentro del contenedor Docker, ubícate en
`backend/miproyecto_django` y ejecuta:

```bash
docker-compose exec web python manage.py test
```

Si trabajas en un entorno local (sin Docker) puedes usar:

```bash
python manage.py test
```

## Variables de entorno requeridas

El proyecto utiliza las siguientes variables (ver `settings.py`):

- `DEBUG`
- `SECRET_KEY`
- `FIELD_ENCRYPTION_KEY`
- `ALLOWED_HOSTS`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

