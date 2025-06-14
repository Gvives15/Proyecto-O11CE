# Generated by Django 5.2.1 on 2025-05-30 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateTimeField(auto_now_add=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('monto_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_final', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('abierta', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], max_length=10)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.CharField(max_length=255)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='caja.caja')),
            ],
        ),
    ]
