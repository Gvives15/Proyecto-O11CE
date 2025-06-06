from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from ...models import Rol, Usuario
from ..permissions_config import PERMISSIONS


class Command(BaseCommand):
    help = "Sincroniza los permisos definidos en permissions_config.py"

    def handle(self, *args, **options):
        user_ct = ContentType.objects.get_for_model(Usuario)

        existing = set(
            Permission.objects.filter(content_type=user_ct).values_list("codename", flat=True)
        )
        defined = set()
        for perms in PERMISSIONS.values():
            defined.update(perms.keys())

        to_delete = existing - defined
        if to_delete:
            Permission.objects.filter(content_type=user_ct, codename__in=to_delete).delete()

        created = updated = 0
        for perms in PERMISSIONS.values():
            for codename, data in perms.items():
                perm, created_flag = Permission.objects.update_or_create(
                    codename=codename,
                    content_type=user_ct,
                    defaults={"name": data["name"]},
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

                for role_name in data.get("roles", []):
                    rol, _ = Rol.objects.get_or_create(nombre=role_name)
                    rol.permisos.add(perm)

        self.stdout.write(
            self.style.SUCCESS(
                f"Permisos sincronizados: {created} creados, {updated} actualizados, {len(to_delete)} eliminados"
            )
        )
