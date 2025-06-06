from django.contrib import admin

from .models import Caja, MovimientoCaja


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "fecha_apertura",
        "fecha_cierre",
        "monto_inicial",
        "monto_final",
        "abierta",
    )
    list_filter = ("abierta", "usuario")
    search_fields = ("usuario__email",)
    date_hierarchy = "fecha_apertura"


@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    list_display = ("id", "caja", "fecha", "tipo", "monto", "descripcion")
    list_filter = ("tipo",)
    search_fields = ("descripcion",)
    date_hierarchy = "fecha"

