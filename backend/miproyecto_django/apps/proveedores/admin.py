from django.contrib import admin
from .models import Proveedor, Compra, DetalleCompra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'telefono', 'email')


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 0


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha', 'total', 'almacen')
    list_filter = ('fecha', 'proveedor')
    search_fields = ('proveedor__nombre',)
    date_hierarchy = 'fecha'
    inlines = [DetalleCompraInline]


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = (
        'compra',
        'producto',
        'cantidad',
        'precio_unitario',
    )
