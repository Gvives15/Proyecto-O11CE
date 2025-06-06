from django.contrib import admin

from .models import Venta, DetalleVenta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fecha",
        "cliente",
        "usuario",
        "total",
        "confirmado",
    )
    list_filter = ("tipo_documento", "confirmado", "fecha")
    search_fields = ("cliente__nombre", "cliente__apellido", "id")
    date_hierarchy = "fecha"
    inlines = [DetalleVentaInline]


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_unitario", "subtotal")
