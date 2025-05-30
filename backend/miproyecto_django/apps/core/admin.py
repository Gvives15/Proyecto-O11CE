from django.contrib import admin
from .models import Auditoria

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'modelo', 'instancia_id', 'accion', 'usuario')
    list_filter = ('modelo', 'accion', 'usuario')
    search_fields = ('modelo', 'instancia_id')
