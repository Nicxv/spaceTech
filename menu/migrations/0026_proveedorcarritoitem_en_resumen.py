# Generated by Django 5.0.4 on 2024-06-27 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0025_proveedorcarritoitem_aceptado'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedorcarritoitem',
            name='en_resumen',
            field=models.BooleanField(default=True),
        ),
    ]
