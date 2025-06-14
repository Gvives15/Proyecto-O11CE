# Generated by Django 5.2.1 on 2025-05-26 08:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='almacen',
            options={'ordering': ['sucursal__nombre', 'nombre'], 'verbose_name': 'Almacén', 'verbose_name_plural': 'Almacenes'},
        ),
        migrations.AlterModelOptions(
            name='empresa',
            options={'ordering': ['nombre'], 'verbose_name': 'Empresa', 'verbose_name_plural': 'Empresas'},
        ),
        migrations.AlterModelOptions(
            name='sucursal',
            options={'ordering': ['empresa__nombre', 'nombre'], 'verbose_name': 'Sucursal', 'verbose_name_plural': 'Sucursales'},
        ),
        migrations.AlterField(
            model_name='almacen',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='almacenes', to='empresa.sucursal'),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sucursales', to='empresa.empresa'),
        ),
    ]
