from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'dni', 'email')
    list_filter = ('nombre',)
