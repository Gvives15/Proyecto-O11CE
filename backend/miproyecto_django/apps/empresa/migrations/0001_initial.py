# Generated by Django 5.2.1 on 2025-05-23 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Empresa Ejemplo', max_length=100)),
                ('cuit', models.CharField(default='00000000000', max_length=13, unique=True)),
                ('direccion', models.CharField(default='Sin dirección', max_length=255)),
                ('contacto', models.CharField(default='contacto@empresa.com', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Sucursal Central', max_length=100)),
                ('direccion', models.CharField(default='Sin dirección', max_length=255)),
                ('ubicacion', models.CharField(blank=True, default='', max_length=255)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Almacén Principal', max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.sucursal')),
            ],
        ),
    ]
