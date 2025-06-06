from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "dni",
        "telefono",
        "email",
        "saldo",
    )
    search_fields = ("nombre", "apellido", "dni", "email")
