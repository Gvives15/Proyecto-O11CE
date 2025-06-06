from django.contrib import admin
from .models import (
    Categoria,
    Subcategoria,
    Producto,
    MovimientoStock,
    AlertaSistema,
)

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Producto)
admin.site.register(MovimientoStock)
admin.site.register(AlertaSistema)
