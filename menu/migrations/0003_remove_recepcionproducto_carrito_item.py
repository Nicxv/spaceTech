# Generated by Django 5.0.4 on 2024-07-01 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_recepcionproducto_precio_venta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recepcionproducto',
            name='carrito_item',
        ),
    ]
