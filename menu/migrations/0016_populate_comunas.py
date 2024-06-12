# Generated by Django 4.2.1 on 2024-06-11 01:29

from django.db import migrations

def populate_comunas(apps, schema_editor):
    Comuna = apps.get_model('menu', 'Comuna')
    comunas_data = [
        {'nombre': 'Huechuraba', 'precio_envio': 1000},
        {'nombre': 'Quilicura', 'precio_envio': 2000},
        {'nombre': 'Recoleta', 'precio_envio': 2000},
        {'nombre': 'Independencia', 'precio_envio': 2000},
        {'nombre': 'Conchalí', 'precio_envio': 2000},
        {'nombre': 'Renca', 'precio_envio': 3000},
        {'nombre': 'Santiago', 'precio_envio': 3000},
        {'nombre': 'Providencia', 'precio_envio': 3000},
        {'nombre': 'Ñuñoa', 'precio_envio': 3000},
        {'nombre': 'Macul', 'precio_envio': 4000},
        {'nombre': 'La Reina', 'precio_envio': 4000},
        {'nombre': 'Peñalolén', 'precio_envio': 5000},
        {'nombre': 'Lo Barnechea', 'precio_envio': 5000},
        {'nombre': 'Las Condes', 'precio_envio': 5000},
        {'nombre': 'Vitacura', 'precio_envio': 5000},
        {'nombre': 'San Miguel', 'precio_envio': 6000},
        {'nombre': 'La Cisterna', 'precio_envio': 6000},
        {'nombre': 'San Joaquín', 'precio_envio': 6000},
        {'nombre': 'La Granja', 'precio_envio': 6000},
        {'nombre': 'El Bosque', 'precio_envio': 7000},
        {'nombre': 'San Bernardo', 'precio_envio': 7000},
        {'nombre': 'Puente Alto', 'precio_envio': 8000},
        {'nombre': 'La Florida', 'precio_envio': 8000},
        {'nombre': 'Maipú', 'precio_envio': 9000},
        {'nombre': 'Pudahuel', 'precio_envio': 9000},
        {'nombre': 'Cerrillos', 'precio_envio': 9000},
        {'nombre': 'Estación Central', 'precio_envio': 9000},
        {'nombre': 'Lo Espejo', 'precio_envio': 9000},
        {'nombre': 'Lo Prado', 'precio_envio': 9000},
        {'nombre': 'Pedro Aguirre Cerda', 'precio_envio': 9000},
        {'nombre': 'San Ramón', 'precio_envio': 9000},
    ]

    for comuna_data in comunas_data:
        Comuna.objects.create(**comuna_data)


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0015_comuna_precio_envio'),
    ]

    operations = [
        migrations.RunPython(populate_comunas),
    ]
