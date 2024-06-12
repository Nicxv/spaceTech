# Generated by Django 5.0.4 on 2024-06-08 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_venta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('comuna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.comuna')),
            ],
        ),
    ]
