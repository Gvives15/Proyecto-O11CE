from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from ...models import CustomPermission, RolePermission
from ..permissions_config import PERMISSIONS

class Command(BaseCommand):
    help = 'Sincroniza los permisos definidos en permissions_config.py con la base de datos'

    def handle(self, *args, **options):
        # Obtener el content type para el modelo Usuario
        user_content_type = ContentType.objects.get(app_label='user', model='usuario')
        
        # Contadores para el reporte
        created = 0
        updated = 0
        deleted = 0
        
        # Obtener todos los permisos existentes
        existing_permissions = set(CustomPermission.objects.values_list('codename', flat=True))
        
        # Obtener todos los códigos de permisos definidos
        defined_permissions = set()
        for category in PERMISSIONS.values():
            defined_permissions.update(category.keys())
        
        # Eliminar permisos que ya no están definidos
        to_delete = existing_permissions - defined_permissions
        if to_delete:
            CustomPermission.objects.filter(codename__in=to_delete).delete()
            deleted = len(to_delete)
            self.stdout.write(f"Eliminados {deleted} permisos obsoletos")
        
        # Crear o actualizar permisos
        for category, perms in PERMISSIONS.items():
            for codename, perm_data in perms.items():
                perm, created_flag = CustomPermission.objects.update_or_create(
                    codename=codename,
                    defaults={
                        'name': perm_data['name'],
                        'description': perm_data['description'],
                        'content_type': user_content_type
                    }
                )
                
                if created_flag:
                    created += 1
                else:
                    updated += 1
                
                # Sincronizar permisos de roles
                for role in perm_data['roles']:
                    RolePermission.objects.get_or_create(
                        rol=role,
                        permission=perm,
                        defaults={'is_active': True}
                    )
        
        # Reporte final
        self.stdout.write(self.style.SUCCESS(
            f"Sincronización completada:\n"
            f"- {created} permisos creados\n"
            f"- {updated} permisos actualizados\n"
            f"- {deleted} permisos eliminados"
        )) 